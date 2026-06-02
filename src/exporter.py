"""
Module 4 — Output and CRM export.

Generates:
  1. master_leads.csv      — All fields, scored, priority-tiered
  2. priority_a_leads.csv  — Top leads only (Priority A)
  3. outreach_sequences.csv — One row per email step per lead
  4. salesforce_import.csv  — Salesforce-compatible column names
  5. linkedin_manual_template.csv — Manual entry template for LinkedIn
  6. linkedin_guide.txt    — Full LinkedIn search guide
  7. irs_guide.txt         — IRS PTIN directory guide

All CSVs are UTF-8 with BOM for Excel compatibility.
"""

import os
import csv
from datetime import datetime

from outreach_templates import get_sequence_for_lead, render_template
from linkedin_queries import print_linkedin_guide, get_all_linkedin_data
from irs_ptin import generate_irs_search_guide
from nysscpa_scraper import generate_nysscpa_guide

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../output")

# Master CSV columns (in display order)
MASTER_COLUMNS = [
    "priority",
    "score",
    "name",
    "address",
    "zip",
    "phone",
    "website",
    "source",
    "founded_year",
    "employee_count",
    "rating",
    "review_count",
    "payroll_on_site",
    "competitor_detected",
    "contact_page",
    "blog_page",
    "services_count",
    "score_notes",
    "entity_type",
    "dos_status",
    "firm_name",
    "credential",
]

SALESFORCE_COLUMN_MAP = {
    "name": "Account Name",
    "address": "Billing Street",
    "zip": "Billing Zip/Postal Code",
    "phone": "Phone",
    "website": "Website",
    "source": "Lead Source",
    "priority": "Rating",
    "score": "ADP_Score__c",
    "payroll_on_site": "Payroll_Detected__c",
    "competitor_detected": "Competitor__c",
    "founded_year": "Year_Founded__c",
    "employee_count": "NumberOfEmployees",
    "review_count": "Review_Count__c",
    "score_notes": "Score_Notes__c",
}


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def write_csv(filename: str, rows: list[dict], columns: list[str]):
    """Write a list of dicts to CSV. Uses BOM for Excel compatibility."""
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})
    print(f"  → Wrote {len(rows)} rows to {path}")
    return path


def export_master_leads(leads: list[dict]) -> str:
    """Export full master lead list."""
    sorted_leads = sorted(leads, key=lambda l: (-l.get("score", 0), l.get("name", "")))
    return write_csv("master_leads.csv", sorted_leads, MASTER_COLUMNS)


def export_priority_a(leads: list[dict]) -> str:
    """Export only Priority A leads."""
    a_leads = [l for l in leads if l.get("priority") == "A"]
    a_leads_sorted = sorted(a_leads, key=lambda l: -l.get("score", 0))
    return write_csv("priority_a_leads.csv", a_leads_sorted, MASTER_COLUMNS)


def export_salesforce(leads: list[dict]) -> str:
    """Export Salesforce-compatible CSV."""
    sf_rows = []
    for lead in leads:
        sf_row = {}
        for src_col, sf_col in SALESFORCE_COLUMN_MAP.items():
            sf_row[sf_col] = lead.get(src_col, "")
        # Salesforce Rating field maps: Hot/Warm/Cold
        priority_to_rating = {"A": "Hot", "B": "Warm", "C": "Cold"}
        sf_row["Rating"] = priority_to_rating.get(lead.get("priority", "C"), "Cold")
        sf_rows.append(sf_row)

    sf_cols = list(SALESFORCE_COLUMN_MAP.values())
    return write_csv("salesforce_import.csv", sf_rows, sf_cols)


def export_outreach_sequences(leads: list[dict], your_info: dict) -> str:
    """
    Export one row per email step per lead.
    Columns: lead_name, firm, priority, track, step, day, channel,
             subject_a, subject_b, body, notes.
    """
    rows = []
    for lead in leads:
        sequence = get_sequence_for_lead(lead)

        # Build merge fields
        name_parts = lead.get("name", "").split()
        first_name = name_parts[0] if name_parts else "there"
        firm_name = lead.get("firm_name") or lead.get("name", "your firm")
        neighborhood = _infer_neighborhood(lead.get("zip", ""))

        merge_fields = {
            "first_name": first_name,
            "firm_name": firm_name,
            "neighborhood": neighborhood,
            **your_info,
        }

        for template in sequence:
            rendered = render_template(template, merge_fields)
            row = {
                "lead_name": lead.get("name", ""),
                "firm_name": firm_name,
                "phone": lead.get("phone", ""),
                "website": lead.get("website", ""),
                "priority": lead.get("priority", "C"),
                "score": lead.get("score", 0),
                **rendered,
            }
            rows.append(row)

    seq_cols = [
        "lead_name", "firm_name", "phone", "website", "priority", "score",
        "track", "step", "day", "channel",
        "subject_a", "subject_b", "subject_c",
        "body", "notes",
    ]
    return write_csv("outreach_sequences.csv", rows, seq_cols)


def export_linkedin_template() -> str:
    """Write LinkedIn manual entry template CSV."""
    columns = [
        "First Name", "Last Name", "Firm Name", "LinkedIn URL",
        "City/Neighborhood", "ZIP", "Phone", "Email",
        "Employee Count", "Founded Year",
        "Payroll Mentioned (yes/no)", "Competitor Detected",
        "Priority (A/B/C)", "Notes",
    ]
    path = os.path.join(OUTPUT_DIR, "linkedin_manual_template.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        # Write 20 blank rows as a starting template
        for _ in range(20):
            writer.writerow([""] * len(columns))
    print(f"  → Wrote LinkedIn template to {path}")
    return path


def export_guides():
    """Write all manual guide text files."""
    ensure_output_dir()

    # LinkedIn guide
    linkedin_path = os.path.join(OUTPUT_DIR, "linkedin_guide.txt")
    with open(linkedin_path, "w", encoding="utf-8") as f:
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = buf = StringIO()
        print_linkedin_guide()
        sys.stdout = old_stdout
        f.write(buf.getvalue())
    print(f"  → Wrote LinkedIn guide to {linkedin_path}")

    # IRS PTIN guide
    irs_path = os.path.join(OUTPUT_DIR, "irs_ptin_guide.txt")
    with open(irs_path, "w", encoding="utf-8") as f:
        f.write(generate_irs_search_guide())
    print(f"  → Wrote IRS PTIN guide to {irs_path}")

    # NYSSCPA guide
    nysscpa_path = os.path.join(OUTPUT_DIR, "nysscpa_guide.txt")
    with open(nysscpa_path, "w", encoding="utf-8") as f:
        f.write(generate_nysscpa_guide())
    print(f"  → Wrote NYSSCPA guide to {nysscpa_path}")


def export_summary_report(leads: list[dict]) -> str:
    """Write a plain-text summary of the run."""
    total = len(leads)
    by_priority = {"A": 0, "B": 0, "C": 0}
    by_source: dict[str, int] = {}
    with_website = 0
    with_payroll = 0
    with_competitor = 0

    for lead in leads:
        p = lead.get("priority", "C")
        by_priority[p] = by_priority.get(p, 0) + 1

        for source in str(lead.get("source", "")).split(", "):
            source = source.strip()
            if source:
                by_source[source] = by_source.get(source, 0) + 1

        if lead.get("website"):
            with_website += 1
        if lead.get("payroll_on_site") == "yes":
            with_payroll += 1
        if lead.get("competitor_detected"):
            with_competitor += 1

    lines = [
        "=" * 60,
        "ADP BROOKLYN PROSPECTING — RUN SUMMARY",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 60,
        "",
        f"Total unique leads:    {total}",
        f"  Priority A (Hot):    {by_priority['A']}",
        f"  Priority B (Warm):   {by_priority['B']}",
        f"  Priority C (Cold):   {by_priority['C']}",
        "",
        f"Leads with website:    {with_website}",
        f"Payroll signal found:  {with_payroll}",
        f"Competitor detected:   {with_competitor}",
        "",
        "Leads by source:",
    ]
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        lines.append(f"  {source:<20} {count}")

    lines += [
        "",
        "Output files:",
        "  output/master_leads.csv",
        "  output/priority_a_leads.csv",
        "  output/outreach_sequences.csv",
        "  output/salesforce_import.csv",
        "  output/linkedin_manual_template.csv",
        "  output/linkedin_guide.txt",
        "  output/irs_ptin_guide.txt",
        "  output/nysscpa_guide.txt",
        "  output/run_summary.txt",
        "",
    ]

    report = "\n".join(lines)
    path = os.path.join(OUTPUT_DIR, "run_summary.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  → Wrote summary to {path}")
    return report


def _infer_neighborhood(zip_code: str) -> str:
    """Map Brooklyn ZIP to neighborhood name for email personalization."""
    ZIP_NEIGHBORHOODS = {
        "11201": "DUMBO/Downtown Brooklyn",
        "11205": "Clinton Hill",
        "11206": "Williamsburg",
        "11207": "East New York",
        "11208": "East New York",
        "11209": "Bay Ridge",
        "11210": "Flatbush",
        "11211": "Williamsburg",
        "11212": "Brownsville",
        "11213": "Crown Heights",
        "11214": "Bensonhurst",
        "11215": "Park Slope",
        "11216": "Crown Heights",
        "11217": "Park Slope",
        "11218": "Kensington",
        "11219": "Borough Park",
        "11220": "Sunset Park",
        "11221": "Bushwick",
        "11222": "Greenpoint",
        "11223": "Gravesend",
        "11224": "Coney Island",
        "11225": "Flatbush",
        "11226": "Flatbush",
        "11228": "Dyker Heights",
        "11229": "Marine Park",
        "11230": "Midwood",
        "11231": "Carroll Gardens",
        "11232": "Sunset Park",
        "11233": "Bed-Stuy",
        "11234": "Flatlands",
        "11235": "Sheepshead Bay",
        "11236": "Canarsie",
        "11237": "Bushwick",
        "11238": "Prospect Heights",
        "11239": "Georgetown/Marine Park",
    }
    return ZIP_NEIGHBORHOODS.get(str(zip_code).strip(), "Brooklyn")
