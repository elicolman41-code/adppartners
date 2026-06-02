"""
Module 1g — Deduplication engine.

Merges leads from all sources into a single master list.
Deduplication strategy:
  1. Exact phone match (normalized 10-digit)
  2. Fuzzy name match (>= 85% similarity) within same ZIP
  3. Website domain match

When a duplicate is found, the records are merged:
  - Sources are combined (e.g. "Google Maps, Yelp")
  - Best available data is kept (non-empty fields win)
  - Higher review count wins
"""

import re
from fuzzywuzzy import fuzz


def normalize_phone(phone: str) -> str:
    """Strip all non-digits, return 10-digit string or empty."""
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits if len(digits) == 10 else ""


def normalize_name(name: str) -> str:
    """Lowercase, strip punctuation, remove common suffixes."""
    suffixes = [
        " llc", " inc", " corp", " ltd", " co", " pc", " pllc",
        " cpa", " cpas", " & associates", " and associates",
        " accounting", " bookkeeping", " tax", " services",
    ]
    n = name.lower().strip()
    n = re.sub(r"[^\w\s]", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    for suffix in suffixes:
        if n.endswith(suffix):
            n = n[: -len(suffix)].strip()
    return n


def extract_domain(url: str) -> str:
    """Extract bare domain from URL."""
    if not url:
        return ""
    url = url.lower().strip()
    url = re.sub(r"^https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    url = url.split("/")[0].split("?")[0]
    return url


def merge_records(existing: dict, new: dict) -> dict:
    """Merge new record into existing, keeping best data."""
    merged = dict(existing)

    # Merge source lists
    sources = set(str(merged.get("source", "")).split(", "))
    new_source = str(new.get("source", ""))
    if new_source:
        sources.add(new_source)
    merged["source"] = ", ".join(sorted(s for s in sources if s))

    # For string fields: keep existing if non-empty, else take new
    for field in ["phone", "website", "address", "zip", "rating", "founded_year",
                  "entity_type", "firm_name"]:
        if not merged.get(field) and new.get(field):
            merged[field] = new[field]

    # For review count: keep the higher number
    try:
        existing_count = int(merged.get("review_count", 0) or 0)
        new_count = int(new.get("review_count", 0) or 0)
        merged["review_count"] = max(existing_count, new_count)
    except (ValueError, TypeError):
        pass

    # For rating: keep the one with more reviews backing it
    if new.get("rating") and new.get("review_count", 0) > existing.get("review_count", 0):
        merged["rating"] = new["rating"]

    return merged


def deduplicate(leads: list[dict]) -> list[dict]:
    """
    Deduplicate a list of lead dicts.
    Returns deduplicated list with merged sources.
    """
    print(f"[Dedup] Starting with {len(leads)} raw leads...")

    # Indexes for fast lookup
    phone_index: dict[str, int] = {}    # normalized_phone → master_list index
    domain_index: dict[str, int] = {}   # domain → master_list index
    master: list[dict] = []

    for lead in leads:
        phone = normalize_phone(lead.get("phone", ""))
        name = normalize_name(lead.get("name", ""))
        domain = extract_domain(lead.get("website", ""))
        zip_code = str(lead.get("zip", "")).strip()

        matched_idx = None

        # 1. Exact phone match
        if phone and phone in phone_index:
            matched_idx = phone_index[phone]

        # 2. Domain match
        if matched_idx is None and domain and domain in domain_index:
            matched_idx = domain_index[domain]

        # 3. Fuzzy name match within same ZIP
        if matched_idx is None and name and zip_code:
            for i, existing in enumerate(master):
                existing_zip = str(existing.get("zip", "")).strip()
                if existing_zip != zip_code:
                    continue
                existing_name = normalize_name(existing.get("name", ""))
                if fuzz.token_sort_ratio(name, existing_name) >= 85:
                    matched_idx = i
                    break

        if matched_idx is not None:
            # Merge into existing record
            master[matched_idx] = merge_records(master[matched_idx], lead)
            # Update indexes with any new data
            if phone:
                phone_index[phone] = matched_idx
            if domain:
                domain_index[domain] = matched_idx
        else:
            # New unique lead
            idx = len(master)
            master.append(dict(lead))
            if phone:
                phone_index[phone] = idx
            if domain:
                domain_index[domain] = idx

    print(f"[Dedup] Reduced to {len(master)} unique leads.")
    return master
