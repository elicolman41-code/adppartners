"""
Module 1b — Yelp Fusion API scraper.

Uses the Business Search endpoint to find accounting/payroll firms in Brooklyn.
Requires YELP_API_KEY in .env.

Docs: https://docs.developer.yelp.com/reference/v3_business_search
"""

import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

from constants import BROOKLYN_ZIPS, SEARCH_TERMS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../config/.env"))

YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
YELP_BUSINESS_URL = "https://api.yelp.com/v3/businesses/{id}"

# Yelp category aliases that map to our targets
YELP_CATEGORIES = [
    "accountants",
    "bookkeepers",
    "payrollservices",
    "taxservices",
]


def search_yelp(api_key: str, term: str, zip_code: str, offset: int = 0) -> dict:
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "term": term,
        "location": f"Brooklyn, NY {zip_code}",
        "limit": 50,
        "offset": offset,
        "sort_by": "best_match",
    }
    resp = requests.get(YELP_SEARCH_URL, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_yelp_details(api_key: str, biz_id: str) -> dict:
    """Get phone, website, founded year hint from business details."""
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(YELP_BUSINESS_URL.format(id=biz_id), headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return {
        "phone": data.get("display_phone", ""),
        "website": data.get("url", ""),  # Yelp page URL; real website requires scraping
        "yelp_url": data.get("url", ""),
    }


def run_yelp_scraper(api_key: Optional[str] = None) -> list[dict]:
    """
    Main entry point. Returns list of raw lead dicts from Yelp.
    Each dict has: name, address, zip, phone, website, rating, review_count, source.
    """
    api_key = api_key or os.getenv("YELP_API_KEY")
    if not api_key or api_key == "your_yelp_api_key_here":
        print("[SKIP] YELP_API_KEY not set — skipping Yelp scraper.")
        return []

    all_leads: list[dict] = []
    seen_ids: set[str] = set()

    total = len(BROOKLYN_ZIPS) * len(SEARCH_TERMS)
    done = 0

    for zip_code in BROOKLYN_ZIPS:
        for term in SEARCH_TERMS:
            done += 1
            print(f"  [{done}/{total}] Yelp: '{term}' in {zip_code}")
            try:
                data = search_yelp(api_key, term, zip_code)
                businesses = data.get("businesses", [])

                for biz in businesses:
                    biz_id = biz.get("id", "")
                    if biz_id in seen_ids:
                        continue
                    seen_ids.add(biz_id)

                    location = biz.get("location", {})
                    address_parts = location.get("display_address", [])
                    address = ", ".join(address_parts)
                    zip_val = location.get("zip_code", zip_code)

                    lead = {
                        "name": biz.get("name", ""),
                        "address": address,
                        "zip": zip_val,
                        "phone": biz.get("display_phone", ""),
                        "website": biz.get("url", ""),
                        "rating": biz.get("rating", ""),
                        "review_count": biz.get("review_count", 0),
                        "source": "Yelp",
                        "yelp_id": biz_id,
                    }
                    all_leads.append(lead)
                    time.sleep(0.05)

            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    print("  [RATE LIMIT] Yelp — sleeping 30s")
                    time.sleep(30)
                else:
                    print(f"  [ERROR] {e}")
            except Exception as e:
                print(f"  [ERROR] {e}")

            time.sleep(0.2)

    print(f"[Yelp] Found {len(all_leads)} unique businesses.")
    return all_leads
