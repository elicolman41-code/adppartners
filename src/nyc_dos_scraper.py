"""
Module 1c — NYC Department of State Entity Search scraper.

Queries https://apps.dos.ny.gov/publicInquiry/ for active LLCs/corps
in Kings County with accounting/bookkeeping/payroll keywords in the name.

This is a form-based site. We POST to the search endpoint and parse the HTML.
No API key required — public data.

NOTE: The DOS site uses ASP.NET viewstate. We fetch the form first to get
__VIEWSTATE, then POST the search. If the site updates its HTML structure,
update the CSS selectors below.
"""

import time
import re
import requests
from bs4 import BeautifulSoup

from constants import NYC_DOS_SEARCH_TERMS

BASE_URL = "https://apps.dos.ny.gov/publicInquiry/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def _get_viewstate(session: requests.Session) -> dict:
    """Fetch the search page and extract ASP.NET hidden fields."""
    resp = session.get(BASE_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    fields = {}
    for hidden in soup.find_all("input", type="hidden"):
        name = hidden.get("name", "")
        if name.startswith("__"):
            fields[name] = hidden.get("value", "")
    return fields


def _search_dos(session: requests.Session, viewstate: dict, keyword: str) -> list[dict]:
    """
    POST a search for `keyword` in Kings County, status Active.
    Returns list of entity dicts: {name, county, type, status, dos_id, date_formed}.
    """
    form_data = {
        **viewstate,
        "ctl00$ContentPlaceHolder1$txtEntityName": keyword,
        "ctl00$ContentPlaceHolder1$ddlCounty": "KINGS",
        "ctl00$ContentPlaceHolder1$ddlEntityType": "",  # All types
        "ctl00$ContentPlaceHolder1$ddlEntityStatus": "ACTIVE",
        "ctl00$ContentPlaceHolder1$btnSearch": "Search",
    }

    resp = session.post(BASE_URL, data=form_data, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    results = []
    # Results appear in a gridview table
    table = soup.find("table", id=re.compile(r"GridView|gvResults", re.I))
    if not table:
        # Try any table with multiple rows
        tables = soup.find_all("table")
        for t in tables:
            rows = t.find_all("tr")
            if len(rows) > 2:
                table = t
                break

    if not table:
        return results

    rows = table.find_all("tr")
    headers_row = rows[0] if rows else None
    col_headers = []
    if headers_row:
        col_headers = [th.get_text(strip=True).lower() for th in headers_row.find_all(["th", "td"])]

    for row in rows[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cells:
            continue

        entity = {}
        if col_headers:
            for i, header in enumerate(col_headers):
                if i < len(cells):
                    entity[header] = cells[i]
        else:
            # Fallback: positional
            entity = {
                "name": cells[0] if len(cells) > 0 else "",
                "dos_id": cells[1] if len(cells) > 1 else "",
                "type": cells[2] if len(cells) > 2 else "",
                "status": cells[3] if len(cells) > 3 else "",
                "county": "KINGS",
                "date_formed": cells[4] if len(cells) > 4 else "",
            }

        entity["search_keyword"] = keyword
        results.append(entity)

    return results


def _normalize_dos_entity(entity: dict) -> dict:
    """Convert raw DOS entity to our standard lead schema."""
    # Map whatever column names DOS uses to our schema
    name = (
        entity.get("entity name", "")
        or entity.get("name", "")
        or entity.get("dos_id", "")
    )
    date_formed = (
        entity.get("date of formation", "")
        or entity.get("date formed", "")
        or entity.get("date_formed", "")
        or entity.get("initial dos filing date", "")
    )
    entity_type = entity.get("entity type", "") or entity.get("type", "")

    founded_year = ""
    if date_formed:
        m = re.search(r"\b(19|20)\d{2}\b", date_formed)
        if m:
            founded_year = m.group(0)

    return {
        "name": name,
        "address": "Brooklyn, NY",
        "zip": "",
        "phone": "",
        "website": "",
        "rating": "",
        "review_count": 0,
        "source": "NYC DOS",
        "founded_year": founded_year,
        "entity_type": entity_type,
        "dos_status": entity.get("status", "ACTIVE"),
    }


def run_nyc_dos_scraper() -> list[dict]:
    """
    Main entry point. Returns list of raw lead dicts from NYC DOS.
    """
    session = requests.Session()
    all_leads = []
    seen_names: set[str] = set()

    for keyword in NYC_DOS_SEARCH_TERMS:
        print(f"  [NYC DOS] Searching: '{keyword}' in Kings County...")
        try:
            viewstate = _get_viewstate(session)
            entities = _search_dos(session, viewstate, keyword)
            print(f"    → {len(entities)} results")

            for entity in entities:
                lead = _normalize_dos_entity(entity)
                key = lead["name"].lower().strip()
                if key and key not in seen_names:
                    seen_names.add(key)
                    all_leads.append(lead)

        except Exception as e:
            print(f"  [ERROR] NYC DOS search for '{keyword}': {e}")

        time.sleep(1.5)  # Polite crawl delay

    print(f"[NYC DOS] Found {len(all_leads)} unique active entities.")
    return all_leads
