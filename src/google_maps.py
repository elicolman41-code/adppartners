"""
Module 1a — Google Maps Places API scraper.

Uses the Places API (Text Search + Place Details) to find accounting/payroll
firms in each Brooklyn zip code. Requires GOOGLE_MAPS_API_KEY in .env.

Docs: https://developers.google.com/maps/documentation/places/web-service/text-search
"""

import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

from constants import BROOKLYN_ZIPS, SEARCH_TERMS

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../config/.env"))

PLACES_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"


def fetch_places_for_query(api_key: str, query: str, zip_code: str) -> list[dict]:
    """Run one text search and paginate through all results (max 60 per query)."""
    results = []
    params = {
        "query": f"{query} Brooklyn NY {zip_code}",
        "key": api_key,
        "type": "establishment",
    }

    while True:
        resp = requests.get(PLACES_TEXT_SEARCH_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") not in ("OK", "ZERO_RESULTS"):
            print(f"  [WARN] Places API status: {data.get('status')} — {data.get('error_message', '')}")
            break

        for place in data.get("results", []):
            results.append({
                "place_id": place.get("place_id", ""),
                "name": place.get("name", ""),
                "address": place.get("formatted_address", ""),
                "rating": place.get("rating", ""),
                "review_count": place.get("user_ratings_total", 0),
                "zip": zip_code,
                "source": "Google Maps",
            })

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

        # Google requires a short delay before next_page_token is valid
        time.sleep(2)
        params = {"pagetoken": next_page_token, "key": api_key}

    return results


def fetch_place_details(api_key: str, place_id: str) -> dict:
    """Get phone + website for a place_id."""
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,website,opening_hours",
        "key": api_key,
    }
    resp = requests.get(PLACES_DETAILS_URL, params=params, timeout=15)
    resp.raise_for_status()
    result = resp.json().get("result", {})
    return {
        "phone": result.get("formatted_phone_number", ""),
        "website": result.get("website", ""),
    }


def run_google_maps_scraper(api_key: Optional[str] = None) -> list[dict]:
    """
    Main entry point. Returns list of raw lead dicts from Google Maps.
    Each dict has: name, address, zip, phone, website, rating, review_count, source.
    """
    api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key or api_key == "your_google_maps_api_key_here":
        print("[SKIP] GOOGLE_MAPS_API_KEY not set — skipping Google Maps scraper.")
        return []

    all_leads: list[dict] = []
    seen_place_ids: set[str] = set()

    total = len(BROOKLYN_ZIPS) * len(SEARCH_TERMS)
    done = 0

    for zip_code in BROOKLYN_ZIPS:
        for term in SEARCH_TERMS:
            done += 1
            print(f"  [{done}/{total}] Google Maps: '{term}' in {zip_code}")
            try:
                places = fetch_places_for_query(api_key, term, zip_code)
                for place in places:
                    pid = place["place_id"]
                    if pid in seen_place_ids:
                        continue
                    seen_place_ids.add(pid)
                    # Fetch phone + website
                    try:
                        details = fetch_place_details(api_key, pid)
                        place.update(details)
                    except Exception as e:
                        print(f"    [WARN] Details fetch failed for {place['name']}: {e}")
                    all_leads.append(place)
                    time.sleep(0.05)  # Stay under QPS limits
            except Exception as e:
                print(f"  [ERROR] {e}")

            time.sleep(0.1)

    print(f"[Google Maps] Found {len(all_leads)} unique places.")
    return all_leads
