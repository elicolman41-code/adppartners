"""
Module 2 — Website qualification and lead scoring.

For each lead with a website, visits the site and scans for:
  - Payroll mentions
  - Competitor mentions (Gusto, Paychex, QuickBooks, etc.)
  - Number of services listed
  - Contact page presence
  - Blog / resources page
  - Founded year language
  - Employee count signals

Scores each lead 1–10 and assigns Priority A / B / C tiers.
"""

import re
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from constants import PAYROLL_KEYWORDS, COMPETITOR_KEYWORDS, SCORE_WEIGHTS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

FETCH_TIMEOUT = 12
MAX_PAGES_PER_SITE = 3  # Home + services + contact


def safe_get(url: str, timeout: int = FETCH_TIMEOUT) -> requests.Response | None:
    """GET with retries and polite error handling."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            return resp
    except Exception:
        pass
    return None


def extract_text(html: str) -> str:
    """Strip HTML tags and return clean text."""
    soup = BeautifulSoup(html, "lxml")
    # Remove script and style elements
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True).lower()


def find_internal_links(html: str, base_url: str) -> list[str]:
    """Find internal page links (services, contact, about, blog)."""
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(base_url).netloc
    interesting_paths = re.compile(
        r"(service|contact|about|team|blog|resource|payroll|pricing)", re.I
    )
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.netloc == base_domain and interesting_paths.search(parsed.path):
            links.append(full_url)
    return list(dict.fromkeys(links))  # dedupe preserving order


def analyze_website(url: str) -> dict:
    """
    Fetch up to MAX_PAGES_PER_SITE pages and return analysis dict.
    """
    result = {
        "payroll_mentioned": False,
        "competitor_detected": "",
        "competitors_found": [],
        "service_count": 0,
        "contact_page": False,
        "blog_page": False,
        "founded_year": "",
        "employee_signals": "",
        "raw_text_length": 0,
        "fetch_error": False,
    }

    if not url or not url.startswith("http"):
        result["fetch_error"] = True
        return result

    # Fetch homepage
    resp = safe_get(url)
    if not resp:
        # Try with www prefix
        parsed = urlparse(url)
        if not parsed.netloc.startswith("www."):
            alt_url = url.replace(parsed.netloc, "www." + parsed.netloc, 1)
            resp = safe_get(alt_url)

    if not resp:
        result["fetch_error"] = True
        return result

    pages_text = extract_text(resp.text)
    result["raw_text_length"] = len(pages_text)

    # Find and fetch additional pages
    internal_links = find_internal_links(resp.text, url)
    for link in internal_links[: MAX_PAGES_PER_SITE - 1]:
        time.sleep(random.uniform(0.3, 0.8))
        sub_resp = safe_get(link)
        if sub_resp:
            pages_text += " " + extract_text(sub_resp.text)

        # Detect contact / blog pages
        lower_link = link.lower()
        if any(w in lower_link for w in ["contact", "reach", "connect", "get-in-touch"]):
            result["contact_page"] = True
        if any(w in lower_link for w in ["blog", "news", "resource", "article", "insight"]):
            result["blog_page"] = True

    # Also detect from homepage links
    for link in internal_links:
        lower = link.lower()
        if any(w in lower for w in ["contact", "reach", "connect"]):
            result["contact_page"] = True
        if any(w in lower for w in ["blog", "news", "resource"]):
            result["blog_page"] = True

    # Check payroll keywords
    for kw in PAYROLL_KEYWORDS:
        if kw in pages_text:
            result["payroll_mentioned"] = True
            break

    # Check competitor keywords
    found_competitors = []
    for comp in COMPETITOR_KEYWORDS:
        if comp.lower() in pages_text:
            found_competitors.append(comp)
    result["competitors_found"] = found_competitors
    result["competitor_detected"] = ", ".join(found_competitors) if found_competitors else ""

    # Count service mentions (rough proxy for firm size)
    service_keywords = [
        "bookkeeping", "accounting", "tax preparation", "tax planning",
        "payroll", "financial statement", "audit", "consulting",
        "business advisory", "controller", "cfo", "fractional",
        "accounts payable", "accounts receivable", "budgeting", "forecasting",
    ]
    service_count = sum(1 for kw in service_keywords if kw in pages_text)
    result["service_count"] = service_count

    # Founded year detection
    year_match = re.search(
        r"(?:founded|established|since|est\.?|in business since)\s+(?:in\s+)?(\b(19|20)\d{2}\b)",
        pages_text,
        re.I,
    )
    if not year_match:
        year_match = re.search(r"©\s*(20\d{2})", pages_text)
    if year_match:
        result["founded_year"] = year_match.group(1) if year_match.lastindex and year_match.lastindex >= 1 else year_match.group(0)

    # Employee count signals in text
    emp_match = re.search(
        r"(\d+)[\s\-]+(?:person|member|employee|staff|professional|associate|team member)",
        pages_text,
        re.I,
    )
    if emp_match:
        result["employee_signals"] = emp_match.group(0)

    return result


def score_lead(lead: dict, analysis: dict) -> dict:
    """
    Score a lead 1–10 based on Module 2 criteria.
    Returns updated lead dict with score, priority, and analysis fields.
    """
    score = 0
    notes = []

    # Payroll mentioned on website (3 pts)
    if analysis.get("payroll_mentioned"):
        score += SCORE_WEIGHTS["payroll_mentioned"]
        notes.append("payroll_on_site")

    # Competitor named (2 pts)
    if analysis.get("competitor_detected"):
        score += SCORE_WEIGHTS["competitor_named"]
        notes.append(f"competitor:{analysis['competitor_detected'][:30]}")

    # Multiple services (1 pt)
    if analysis.get("service_count", 0) >= 3:
        score += SCORE_WEIGHTS["multiple_services"]
        notes.append("multi_service")

    # Contact page (1 pt)
    if analysis.get("contact_page"):
        score += SCORE_WEIGHTS["contact_page"]
        notes.append("contact_page")

    # Founded after 2015 (1 pt)
    founded = analysis.get("founded_year") or lead.get("founded_year", "")
    try:
        if int(founded) >= 2015:
            score += SCORE_WEIGHTS["founded_after_2015"]
            notes.append(f"founded_{founded}")
    except (ValueError, TypeError):
        pass

    # Employee count 2–10 (1 pt)
    try:
        emp_count = int(lead.get("employee_count", 0) or 0)
        if 2 <= emp_count <= 10:
            score += SCORE_WEIGHTS["employee_count_2_10"]
            notes.append("emp_2_10")
    except (ValueError, TypeError):
        pass

    # Review count over 10 (1 pt)
    try:
        reviews = int(lead.get("review_count", 0) or 0)
        if reviews >= 10:
            score += SCORE_WEIGHTS["review_count_over_10"]
            notes.append(f"reviews_{reviews}")
    except (ValueError, TypeError):
        pass

    # Assign priority tier
    if score >= 7:
        priority = "A"
    elif score >= 4:
        priority = "B"
    else:
        priority = "C"

    lead = dict(lead)
    lead["score"] = score
    lead["priority"] = priority
    lead["score_notes"] = "; ".join(notes)
    lead["payroll_on_site"] = "yes" if analysis.get("payroll_mentioned") else "no"
    lead["competitor_detected"] = analysis.get("competitor_detected", "")
    lead["contact_page"] = "yes" if analysis.get("contact_page") else "no"
    lead["blog_page"] = "yes" if analysis.get("blog_page") else "no"
    lead["services_count"] = analysis.get("service_count", 0)
    if analysis.get("founded_year") and not lead.get("founded_year"):
        lead["founded_year"] = analysis["founded_year"]

    return lead


def run_website_scorer(leads: list[dict], delay_range: tuple = (0.5, 1.5)) -> list[dict]:
    """
    Main entry point. Scores all leads that have a website.
    Leads without websites get scored on available data only.
    Returns updated lead list.
    """
    total = len(leads)
    print(f"[Scorer] Scoring {total} leads...")

    scored = []
    has_site = sum(1 for l in leads if l.get("website"))
    print(f"[Scorer] {has_site} leads have websites to analyze.")

    for i, lead in enumerate(leads):
        website = lead.get("website", "")
        if website:
            print(f"  [{i+1}/{total}] Analyzing: {lead.get('name', 'unknown')} — {website[:50]}")
            try:
                analysis = analyze_website(website)
                if analysis.get("fetch_error"):
                    print(f"    [SKIP] Could not fetch website")
                    analysis = {}
            except Exception as e:
                print(f"    [ERROR] {e}")
                analysis = {}
        else:
            analysis = {}

        scored_lead = score_lead(lead, analysis)
        scored.append(scored_lead)

        if website:
            time.sleep(random.uniform(*delay_range))

    # Stats
    priority_counts = {"A": 0, "B": 0, "C": 0}
    for l in scored:
        priority_counts[l.get("priority", "C")] += 1
    print(
        f"[Scorer] Done. Priority A: {priority_counts['A']}, "
        f"B: {priority_counts['B']}, C: {priority_counts['C']}"
    )

    return scored
