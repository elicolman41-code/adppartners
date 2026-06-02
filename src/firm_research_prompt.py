"""
Master firm intelligence prompt generator.

Given a firm name (and optionally a website/location), generates a
comprehensive AI research prompt you can paste into Claude, ChatGPT,
or Perplexity to quickly profile any individual firm before outreach.

Also generates a ranked priority list based on all available research,
incorporating the key signals from the deep research report:
  - QuickBooks Desktop usage (highest urgency)
  - Retirement-adjacent solo firm (Grid/buyout candidate)
  - Cloud-forward + Gusto/competitor user (Revenue Share candidate)
  - Social media activity signals
  - Review volume and sentiment
"""

from typing import Optional


MASTER_RESEARCH_PROMPT_TEMPLATE = """
You are a B2B sales intelligence analyst. I need a complete profile of the
following accounting/bookkeeping/CPA firm before I reach out to them.

FIRM: {firm_name}
WEBSITE: {website}
LOCATION: {location}
KNOWN PHONE: {phone}

Please research and answer ALL of the following. If you cannot find a piece
of information, say "Not found" — do not guess.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1 — FIRM BASICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Full legal business name and DBA (if any)
2. Year founded (check: website "About" page, NYC DOS entity search, LinkedIn)
3. Owner/founder name(s) — first and last name
4. Estimated number of employees (LinkedIn "About" section, website team page, or Yelp listing)
5. Physical address and ZIP code
6. Phone number(s) listed publicly
7. Email address(es) listed publicly
8. Website URL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2 — SERVICES & PAYROLL SIGNAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. Does the firm explicitly offer payroll processing as a service? (yes/no/unclear)
   If yes, how is it described — full-service, software-only, advisory only?

10. Does the website mention any of these payroll platforms?
    - Gusto, QuickBooks Payroll, Paychex, AMS, Heartland, Rippling,
      Justworks, OnPay, SurePayroll, Square Payroll
    List all mentions found.

11. Is there any language indicating they process payroll IN-HOUSE for clients
    (vs. referring clients out to a third party)?

12. Full list of all services mentioned on the website

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3 — GROWTH & TECH SIGNALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. Does the website have a blog or resources section? When was the last post?

14. Is there a contact page with a form (vs. just a phone number)?

15. Does the website appear modern and recently updated, or dated?
    (Look at copyright year, design, whether it's mobile-responsive)

16. Does the firm use any cloud-first language ("remote", "cloud", "online",
    "paperless", "digital", "Xero", "QuickBooks Online")?

17. Does the website mention AI, automation, or technology tools?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4 — RETIREMENT / EXIT SIGNALS (for buyout pitch)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
18. Does the owner appear to be 50+ years old?
    (Check: LinkedIn profile photo, grad year, founding year of the firm,
    any "established in" language suggesting a long-running practice)

19. Is there any succession plan language on the website
    ("join our team", "we're growing", "associate positions available")?
    Or conversely, is it clearly a solo/owner-operated shop?

20. When was the owner's LinkedIn profile last updated? (Inactive = signal)

21. Does the firm appear to be actively marketing for new clients
    (Google Ads running, active social media, recent blog posts)?
    Or does it look like a "steady state" practice with no growth push?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5 — REVIEWS & REPUTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
22. Google review count and average rating

23. Yelp review count and average rating

24. Do any reviews specifically mention payroll? Quote the relevant text.

25. Do any reviews mention a specific payroll software (Gusto, QuickBooks,
    Paychex, etc.)? Quote the relevant text.

26. Are there any negative reviews about payroll errors or tax filing mistakes?
    (This indicates payroll stress — they may want to offload it)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6 — SOCIAL MEDIA PRESENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
27. LinkedIn company page: exists? Follower count? Last post date?
    Does their LinkedIn description mention payroll?

28. Instagram: exists? Handle? Last post date? Bio text?

29. Facebook business page: exists? Last post date? Services listed?

30. Nextdoor or local directory listings (Patch, Brooklyn Paper, etc.)?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7 — OWNER CONTACT INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
31. Owner's LinkedIn profile URL (search: "[owner name] [firm name] CPA Brooklyn")

32. Owner's direct email (look for: website contact page, LinkedIn contact info,
    email format pattern based on any visible firm emails, NY State CPA license
    directory at https://aca.dos.ny.gov/aca/ )

33. Best contact method for this owner based on what's publicly available:
    (cold email / LinkedIn DM / phone call / walk-in / Instagram DM)

34. Is the owner active on any social platforms? Quote any recent public posts
    that indicate they're open to business conversations.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 8 — PITCH RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on everything above, answer:

35. TRACK RECOMMENDATION:
    • Track 1 (Grid/Buyout) — if: confirmed payroll clients, retirement signals,
      solo or small legacy practice, low reinvestment in growth
    • Track 2 (Revenue Share) — if: cloud-forward, growth-oriented, competitor user,
      founded after 2015, actively marketing
    • Track 3 (Cold/Qualify) — if: unclear whether they do payroll, minimal data

36. TOP 3 TALKING POINTS for this specific firm
    (based on their actual website, reviews, and social media — not generic)

37. BEST OPENING LINE for the first email or call to this firm
    (specific to something you found — not a template)

38. RISK FLAGS: Is there anything that suggests this firm is a bad fit?
    (ADP client already, franchise operation, dormant business, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT YOUR RESPONSE AS:
  - Answer each question by number
  - Keep each answer to 1–3 sentences max
  - Put a ✅ before confirmed facts (found in a primary source)
  - Put a ⚠️ before inferred/estimated facts
  - Put a ❌ before "Not found"
  - At the end, give a one-paragraph EXECUTIVE SUMMARY of this firm
    and whether they're worth pursuing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def generate_firm_prompt(
    firm_name: str,
    website: str = "",
    location: str = "Brooklyn, NY",
    phone: str = "",
) -> str:
    """Generate the research prompt for a specific firm."""
    return MASTER_RESEARCH_PROMPT_TEMPLATE.format(
        firm_name=firm_name or "[Unknown]",
        website=website or "[Unknown — please search]",
        location=location or "Brooklyn, NY",
        phone=phone or "[Unknown — please search]",
    )


# ─────────────────────────────────────────────────────────────────────────────
# Priority ranking based on deep research findings
# ─────────────────────────────────────────────────────────────────────────────

PRIORITY_SIGNALS = {
    # Highest urgency signals (from deep research)
    "quickbooks_desktop": {
        "weight": 4,
        "keywords": ["quickbooks desktop", "qbdt", "quickbooks pro", "quickbooks premier",
                     "desktop payroll"],
        "description": "QB Desktop user — displacement event in progress (Oct 2024 sunset)",
    },
    "solo_legacy": {
        "weight": 3,
        "keywords": [],  # Inferred from founding year + employee count
        "description": "Solo/2-person firm founded pre-2010 — likely retirement-adjacent",
    },
    "payroll_confirmed": {
        "weight": 3,
        "keywords": ["payroll processing", "payroll services", "payroll management",
                     "full service payroll", "payroll clients", "we process payroll"],
        "description": "Explicitly confirms payroll processing for clients",
    },
    "gusto_user": {
        "weight": 2,
        "keywords": ["gusto"],
        "description": "Gusto user — pricing pressure, capped revenue share (20% vs ADP 75%)",
    },
    "paychex_user": {
        "weight": 1,
        "keywords": ["paychex"],
        "description": "Paychex user — lower urgency but comparable pitch angle",
    },
    "cloud_forward": {
        "weight": 2,
        "keywords": ["xero", "quickbooks online", "cloud accounting", "remote",
                     "paperless", "digital", "modern accounting"],
        "description": "Cloud-forward firm — receptive to tech-enabled revenue programs",
    },
    "founded_recently": {
        "weight": 1,
        "keywords": [],  # Inferred from founded year
        "description": "Founded 2015+ — growth-oriented, not legacy entrenched",
    },
    "advisory_services": {
        "weight": 1,
        "keywords": ["cfo advisory", "fractional cfo", "business advisory",
                     "strategic planning", "consulting"],
        "description": "Offers advisory — already thinking beyond compliance billing",
    },
    "negative_payroll_reviews": {
        "weight": 2,
        "keywords": [],  # Inferred from review analysis
        "description": "Negative payroll reviews — firm is stressed by payroll; wants relief",
    },
}


def compute_priority_score_from_text(text: str, founded_year: str = "",
                                     employee_count: int = 0) -> tuple[int, list[str]]:
    """
    Compute a priority score from any text blob (website, reviews, bio).
    Returns (score, list_of_triggered_signals).
    """
    text_lower = text.lower()
    score = 0
    signals = []

    for signal_name, config in PRIORITY_SIGNALS.items():
        for kw in config["keywords"]:
            if kw in text_lower:
                score += config["weight"]
                signals.append(f"{signal_name} (+{config['weight']}): {config['description']}")
                break  # Only count each signal once

    # Founded year bonus
    try:
        year = int(founded_year)
        if year < 2010:
            score += PRIORITY_SIGNALS["solo_legacy"]["weight"]
            signals.append(f"solo_legacy (+{PRIORITY_SIGNALS['solo_legacy']['weight']}): founded {year} — pre-2010 practice")
        elif year >= 2015:
            score += PRIORITY_SIGNALS["founded_recently"]["weight"]
            signals.append(f"founded_recently (+{PRIORITY_SIGNALS['founded_recently']['weight']}): founded {year}")
    except (ValueError, TypeError):
        pass

    return score, signals


def generate_ranked_target_list(leads: list[dict]) -> list[dict]:
    """
    Re-rank leads using the deep research priority signals.
    Adds 'research_priority_score' and 'research_signals' fields.
    """
    ranked = []
    for lead in leads:
        # Build text blob from all available text fields
        text_blob = " ".join([
            str(lead.get("name", "")),
            str(lead.get("score_notes", "")),
            str(lead.get("competitor_detected", "")),
            str(lead.get("payroll_on_site", "")),
        ])

        score, signals = compute_priority_score_from_text(
            text_blob,
            founded_year=str(lead.get("founded_year", "")),
            employee_count=int(lead.get("employee_count", 0) or 0),
        )

        lead = dict(lead)
        lead["research_priority_score"] = score
        lead["research_signals"] = "; ".join(signals[:3])  # Top 3 signals
        ranked.append(lead)

    # Sort: existing score first, then research priority
    ranked.sort(key=lambda l: (
        -(l.get("score", 0) + l.get("research_priority_score", 0))
    ))
    return ranked


def print_firm_prompt(firm_name: str, website: str = "", phone: str = ""):
    """Print the research prompt for a firm to stdout."""
    prompt = generate_firm_prompt(firm_name, website, phone=phone)
    print(prompt)
    print(f"\n{'─'*70}")
    print("PASTE THE ABOVE INTO: claude.ai, chatgpt.com, or perplexity.ai")
    print(f"{'─'*70}\n")


if __name__ == "__main__":
    import sys
    firm = sys.argv[1] if len(sys.argv) > 1 else "Brooklyn CPA LLC"
    site = sys.argv[2] if len(sys.argv) > 2 else ""
    phone = sys.argv[3] if len(sys.argv) > 3 else ""
    print_firm_prompt(firm, site, phone)
