"""
Module 1f — NYSSCPA Member Directory scraper.

The NYSSCPA Find-a-CPA directory is at: https://www.nysscpa.org/find-a-cpa
It uses a JavaScript-rendered search form. This module:
  1. Attempts a direct HTTP search (works if the backend is a REST API)
  2. Falls back to a manual guide + Selenium skeleton

The directory lets you filter by: practice area, county (Kings = Brooklyn),
firm size, and services offered.
"""

import time
import requests
from bs4 import BeautifulSoup

NYSSCPA_SEARCH_URL = "https://www.nysscpa.org/find-a-cpa"
# The actual API endpoint (may require inspection via browser DevTools)
NYSSCPA_API_URL = "https://www.nysscpa.org/api/find-a-cpa/search"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nysscpa.org/find-a-cpa",
}


def attempt_nysscpa_api_search() -> list[dict]:
    """
    Try to hit the NYSSCPA JSON API directly. This works if the frontend
    calls a discoverable REST endpoint. Inspect Network tab in DevTools
    at https://www.nysscpa.org/find-a-cpa to confirm the current endpoint.
    """
    payload = {
        "county": "Kings",          # Brooklyn
        "services": [],              # All services
        "firmSize": "",
        "page": 1,
        "pageSize": 100,
    }

    results = []
    try:
        resp = requests.post(NYSSCPA_API_URL, json=payload, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            members = data.get("results", data.get("members", data.get("data", [])))
            for m in members:
                results.append({
                    "name": (
                        f"{m.get('firstName', '')} {m.get('lastName', '')}".strip()
                        or m.get("name", "")
                        or m.get("firmName", "")
                    ),
                    "address": m.get("address", ""),
                    "zip": m.get("zip", m.get("zipCode", "")),
                    "phone": m.get("phone", m.get("phoneNumber", "")),
                    "website": m.get("website", m.get("url", "")),
                    "rating": "",
                    "review_count": 0,
                    "source": "NYSSCPA",
                    "firm_name": m.get("firmName", m.get("firm", "")),
                    "credential": "CPA",
                })
            print(f"[NYSSCPA] API returned {len(results)} results.")
        else:
            print(f"[NYSSCPA] API returned {resp.status_code} — falling back to manual guide.")
    except Exception as e:
        print(f"[NYSSCPA] API attempt failed: {e}")

    return results


def generate_nysscpa_guide() -> str:
    lines = [
        "=" * 70,
        "NYSSCPA FIND-A-CPA DIRECTORY — MANUAL SEARCH GUIDE",
        "=" * 70,
        "",
        "URL: https://www.nysscpa.org/find-a-cpa",
        "",
        "STEP-BY-STEP:",
        "  1. Open the URL above",
        "  2. In 'County', select: Kings (= Brooklyn)",
        "  3. In 'Services', check: Payroll, Accounting/Auditing, Bookkeeping",
        "  4. Click Search",
        "  5. For each result, record: Name, Firm, Phone, Website, Address",
        "  6. Export to output/nysscpa_manual.csv",
        "",
        "DEVTOOLS TIP (find the API endpoint):",
        "  1. Open Chrome DevTools → Network tab → filter 'XHR'",
        "  2. Perform a search on the site",
        "  3. Look for a request to /api/ or /search/",
        "  4. Copy the request URL and payload",
        "  5. Update NYSSCPA_API_URL in src/nysscpa_scraper.py",
        "",
        "COLUMNS TO CAPTURE:",
        "  - Member Name",
        "  - Firm Name",
        "  - Phone",
        "  - Website",
        "  - City, ZIP",
        "  - Services (note if Payroll is listed)",
        "",
    ]
    return "\n".join(lines)


def run_nysscpa_scraper() -> list[dict]:
    results = attempt_nysscpa_api_search()
    if not results:
        guide = generate_nysscpa_guide()
        print(guide)
        print("[NYSSCPA] No automated results. See guide above for manual steps.")
    return results
