"""
Salesforce deduplication module.

Takes your exported Salesforce list (86 existing accounts) and removes any
firm from the master lead list that you already have in your CRM.

HOW TO EXPORT YOUR SF LIST:
  1. In Salesforce → Accounts (or Leads) → All Records
  2. Click the gear icon → Export
  3. Select CSV, UTF-8 encoding
  4. Save as: config/salesforce_existing.csv
  5. Run: python src/main.py --sf-existing config/salesforce_existing.csv

The deduplicator uses the same fuzzy-match logic as the main dedup engine:
  - Phone number (normalized 10-digit)
  - Website domain
  - Fuzzy firm name (≥85%) within same ZIP
"""

import csv
import os
from deduplicator import normalize_phone, normalize_name, extract_domain
from fuzzywuzzy import fuzz


def load_salesforce_existing(path: str) -> list[dict]:
    """
    Load existing Salesforce records from a CSV export.
    Handles both Lead and Account export formats.
    """
    if not os.path.exists(path):
        print(f"[SF Dedup] File not found: {path}")
        return []

    records = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(dict(row))

    print(f"[SF Dedup] Loaded {len(records)} existing Salesforce records from {path}")
    return records


def _extract_sf_key_fields(record: dict) -> dict:
    """
    Extract normalized key fields from a Salesforce record.
    Handles both Lead format (FirstName, LastName, Company, Phone, Website)
    and Account format (Name, Phone, Website, BillingPostalCode).
    """
    # Account format
    name = (
        record.get("Name", "")
        or record.get("Account Name", "")
        or f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()
        or record.get("Company", "")
    )
    phone = (
        record.get("Phone", "")
        or record.get("MobilePhone", "")
        or record.get("Mobile", "")
        or record.get("Phone Number", "")
    )
    website = (
        record.get("Website", "")
        or record.get("Web Site", "")
        or record.get("URL", "")
    )
    zip_code = (
        record.get("BillingPostalCode", "")
        or record.get("Postal Code", "")
        or record.get("Zip", "")
        or record.get("Mailing Zip/Postal Code", "")
    )

    return {
        "name": name,
        "phone": normalize_phone(phone),
        "domain": extract_domain(website),
        "norm_name": normalize_name(name),
        "zip": str(zip_code).strip(),
    }


def filter_existing_sf_leads(
    new_leads: list[dict],
    sf_records: list[dict],
    similarity_threshold: int = 85,
) -> tuple[list[dict], list[dict]]:
    """
    Splits new_leads into:
      - net_new:   leads NOT found in Salesforce (safe to prospect)
      - already_in_sf: leads that match an existing SF record

    Returns (net_new, already_in_sf).
    """
    if not sf_records:
        return new_leads, []

    # Build SF lookup indexes
    sf_phones: set[str] = set()
    sf_domains: set[str] = set()
    sf_name_zip: list[tuple[str, str]] = []  # (norm_name, zip)

    for rec in sf_records:
        keys = _extract_sf_key_fields(rec)
        if keys["phone"]:
            sf_phones.add(keys["phone"])
        if keys["domain"]:
            sf_domains.add(keys["domain"])
        if keys["norm_name"] and keys["zip"]:
            sf_name_zip.append((keys["norm_name"], keys["zip"]))

    net_new = []
    already_in_sf = []

    for lead in new_leads:
        phone = normalize_phone(lead.get("phone", ""))
        domain = extract_domain(lead.get("website", ""))
        norm_name = normalize_name(lead.get("name", ""))
        zip_code = str(lead.get("zip", "")).strip()

        matched = False

        if phone and phone in sf_phones:
            matched = True
        elif domain and domain in sf_domains:
            matched = True
        else:
            for sf_name, sf_zip in sf_name_zip:
                if sf_zip != zip_code:
                    continue
                if fuzz.token_sort_ratio(norm_name, sf_name) >= similarity_threshold:
                    matched = True
                    break

        if matched:
            already_in_sf.append(lead)
        else:
            net_new.append(lead)

    print(
        f"[SF Dedup] {len(new_leads)} leads → "
        f"{len(net_new)} net new, "
        f"{len(already_in_sf)} already in Salesforce."
    )
    return net_new, already_in_sf


def enrich_from_salesforce(
    new_leads: list[dict],
    sf_records: list[dict],
) -> list[dict]:
    """
    For leads that ARE in Salesforce, pull in any useful data that SF has
    (owner name, last activity date, existing opportunity, etc.)
    and add a 'sf_status' field so you know not to cold-prospect them.
    """
    enriched = []
    sf_keys = [_extract_sf_key_fields(rec) for rec in sf_records]

    for lead in new_leads:
        phone = normalize_phone(lead.get("phone", ""))
        domain = extract_domain(lead.get("website", ""))
        norm_name = normalize_name(lead.get("name", ""))
        zip_code = str(lead.get("zip", "")).strip()

        sf_match = None
        for i, keys in enumerate(sf_keys):
            if phone and keys["phone"] == phone:
                sf_match = sf_records[i]
                break
            if domain and keys["domain"] == domain:
                sf_match = sf_records[i]
                break
            if (
                keys["zip"] == zip_code
                and fuzz.token_sort_ratio(norm_name, keys["norm_name"]) >= 85
            ):
                sf_match = sf_records[i]
                break

        lead = dict(lead)
        if sf_match:
            lead["sf_status"] = "In CRM"
            lead["sf_owner"] = (
                sf_match.get("Owner", "")
                or sf_match.get("Account Owner", "")
                or sf_match.get("Lead Owner", "")
            )
            lead["sf_last_activity"] = (
                sf_match.get("Last Activity Date", "")
                or sf_match.get("Last Activity", "")
            )
        else:
            lead["sf_status"] = "Net New"
            lead["sf_owner"] = ""
            lead["sf_last_activity"] = ""

        enriched.append(lead)

    return enriched
