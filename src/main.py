"""
ADP Brooklyn Prospecting System — Main Orchestrator

Usage:
    python src/main.py [--skip-google] [--skip-yelp] [--skip-dos]
                       [--skip-nysscpa] [--skip-scoring]
                       [--input-csv PATH]

Steps:
    1. Lead discovery (Google Maps, Yelp, NYC DOS, NYSSCPA)
    2. Deduplication
    3. Website scoring
    4. Export (CSV + guides)

Set your API keys in config/.env before running.
"""

import os
import sys
import argparse
import json
from datetime import datetime
from dotenv import load_dotenv

# Allow imports from src/
sys.path.insert(0, os.path.dirname(__file__))

from constants import OUTPUT_DIR
from deduplicator import deduplicate
from exporter import (
    ensure_output_dir, export_master_leads, export_priority_a,
    export_salesforce, export_outreach_sequences,
    export_linkedin_template, export_guides, export_summary_report,
)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../config/.env"))


def parse_args():
    parser = argparse.ArgumentParser(description="ADP Brooklyn Prospecting System")
    parser.add_argument("--skip-google", action="store_true", help="Skip Google Maps scraper")
    parser.add_argument("--skip-yelp", action="store_true", help="Skip Yelp scraper")
    parser.add_argument("--skip-dos", action="store_true", help="Skip NYC DOS scraper")
    parser.add_argument("--skip-nysscpa", action="store_true", help="Skip NYSSCPA scraper")
    parser.add_argument("--skip-scoring", action="store_true", help="Skip website scoring (faster)")
    parser.add_argument("--input-csv", type=str, default=None,
                        help="Load existing leads from CSV instead of scraping")
    parser.add_argument("--your-name", type=str, default=os.getenv("YOUR_NAME", "[Your Name]"))
    parser.add_argument("--your-email", type=str, default=os.getenv("YOUR_EMAIL", "[Your Email]"))
    parser.add_argument("--your-phone", type=str, default=os.getenv("YOUR_PHONE", "[Your Phone]"))
    return parser.parse_args()


def load_csv_leads(path: str) -> list[dict]:
    """Load leads from an existing CSV file."""
    import csv
    leads = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(dict(row))
    print(f"[Input] Loaded {len(leads)} leads from {path}")
    return leads


def run(args):
    ensure_output_dir()

    print("\n" + "=" * 60)
    print("ADP BROOKLYN PROSPECTING SYSTEM")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")

    all_raw_leads: list[dict] = []

    # ── MODULE 1: Discovery ──────────────────────────────────────────────────

    if args.input_csv:
        all_raw_leads = load_csv_leads(args.input_csv)
    else:
        if not args.skip_google:
            print("\n[Step 1a] Google Maps Places API...")
            from google_maps import run_google_maps_scraper
            leads = run_google_maps_scraper()
            all_raw_leads.extend(leads)
            print(f"  → {len(leads)} leads from Google Maps")
        else:
            print("[Step 1a] Skipping Google Maps.")

        if not args.skip_yelp:
            print("\n[Step 1b] Yelp Fusion API...")
            from yelp_scraper import run_yelp_scraper
            leads = run_yelp_scraper()
            all_raw_leads.extend(leads)
            print(f"  → {len(leads)} leads from Yelp")
        else:
            print("[Step 1b] Skipping Yelp.")

        if not args.skip_dos:
            print("\n[Step 1c] NYC Department of State entity search...")
            from nyc_dos_scraper import run_nyc_dos_scraper
            leads = run_nyc_dos_scraper()
            all_raw_leads.extend(leads)
            print(f"  → {len(leads)} leads from NYC DOS")
        else:
            print("[Step 1c] Skipping NYC DOS.")

        if not args.skip_nysscpa:
            print("\n[Step 1d] NYSSCPA directory...")
            from nysscpa_scraper import run_nysscpa_scraper
            leads = run_nysscpa_scraper()
            all_raw_leads.extend(leads)
            print(f"  → {len(leads)} leads from NYSSCPA")
        else:
            print("[Step 1d] Skipping NYSSCPA.")

    if not all_raw_leads:
        print("\n[WARN] No leads collected. Check your API keys in config/.env")
        print("       Or use --input-csv to load existing leads.")
        print("\nGenerating guides anyway...\n")

    # ── MODULE 1g: Deduplication ─────────────────────────────────────────────

    print("\n[Step 1g] Deduplicating leads...")
    unique_leads = deduplicate(all_raw_leads) if all_raw_leads else []

    # Save raw deduplicated leads before scoring
    raw_path = os.path.join(os.path.dirname(__file__), "../output/raw_leads_pre_scoring.json")
    with open(raw_path, "w") as f:
        json.dump(unique_leads, f, indent=2, default=str)
    print(f"  → Saved {len(unique_leads)} pre-scoring leads to raw_leads_pre_scoring.json")

    # ── MODULE 2: Scoring ────────────────────────────────────────────────────

    if not args.skip_scoring and unique_leads:
        print("\n[Step 2] Website scoring and qualification...")
        print("  This step visits each lead's website. May take a while.")
        from website_scorer import run_website_scorer
        scored_leads = run_website_scorer(unique_leads)
    else:
        if args.skip_scoring:
            print("\n[Step 2] Skipping website scoring.")
        # Score without website analysis (data-only scoring)
        from website_scorer import score_lead
        scored_leads = [score_lead(lead, {}) for lead in unique_leads]

    # ── MODULE 4: Export ──────────────────────────────────────────────────────

    print("\n[Step 4] Exporting outputs...")

    your_info = {
        "your_name": args.your_name,
        "your_email": args.your_email,
        "your_phone": args.your_phone,
        "your_linkedin": os.getenv("YOUR_LINKEDIN", "[Your LinkedIn]"),
    }

    if scored_leads:
        export_master_leads(scored_leads)
        export_priority_a(scored_leads)
        export_salesforce(scored_leads)
        export_outreach_sequences(scored_leads, your_info)

    export_linkedin_template()
    export_guides()

    if scored_leads:
        report = export_summary_report(scored_leads)
        print("\n" + report)
    else:
        print("\n[Done] No leads to export. Guides written to output/")

    print("\n" + "=" * 60)
    print("DONE. Check the output/ folder for all files.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run(parse_args())
