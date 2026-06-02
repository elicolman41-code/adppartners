"""
Module 1d — LinkedIn search URL generator.

LinkedIn does not provide a public API for company/people search.
This module generates ready-to-use search URLs for:
  1. Sales Navigator (if you have a license)
  2. Standard LinkedIn company search
  3. LinkedIn People search

Open these URLs in your browser while logged into LinkedIn.
Results should be reviewed manually and can be entered into the CSV template.

Also outputs a plain-text prospecting guide for LinkedIn manual search.
"""

from constants import COMPETITOR_KEYWORDS

# Brooklyn neighborhoods to search by keyword (LinkedIn doesn't have ZIP filter)
BROOKLYN_NEIGHBORHOODS = [
    "Brooklyn", "Williamsburg", "Park Slope", "Bay Ridge", "Flatbush",
    "Crown Heights", "Bushwick", "Sunset Park", "Borough Park", "Greenpoint",
    "DUMBO", "Cobble Hill", "Carroll Gardens", "Bensonhurst", "Sheepshead Bay",
    "Canarsie", "East Flatbush", "Flatlands", "Marine Park", "Midwood",
    "Prospect Heights", "Bed-Stuy", "Bedford-Stuyvesant",
]

LINKEDIN_COMPANY_INDUSTRIES = [
    "Accounting",
    "Financial Services",
]


def generate_company_search_urls() -> list[dict]:
    """
    Generate LinkedIn company search URLs.
    Returns list of {label, url, instructions}.
    """
    urls = []

    # Standard LinkedIn company search (no Sales Nav required)
    base = "https://www.linkedin.com/search/results/companies/"
    for neighborhood in ["Brooklyn", "Williamsburg", "Park Slope", "Bay Ridge",
                         "Flatbush", "Crown Heights", "Bushwick", "Sunset Park"]:
        for industry_kw in ["accounting", "bookkeeping", "payroll", "CPA"]:
            query = f"{industry_kw} {neighborhood} New York"
            url = (
                f"{base}?keywords={query.replace(' ', '%20')}"
                f"&origin=SWITCH_SEARCH_VERTICAL"
            )
            urls.append({
                "label": f"Company Search: {industry_kw} in {neighborhood}",
                "url": url,
                "type": "company",
                "note": "Filter by: Company size 1–10 employees, Industry: Accounting",
            })

    return urls


def generate_people_search_urls() -> list[dict]:
    """Generate LinkedIn people search URLs for decision-makers."""
    urls = []
    base = "https://www.linkedin.com/search/results/people/"

    titles = ["CPA", "accountant", "bookkeeper", "owner", "principal", "founder"]
    for title in titles:
        query = f"{title} payroll Brooklyn"
        url = (
            f"{base}?keywords={query.replace(' ', '%20')}"
            f"&geoUrn=%5B%22103886785%22%5D"  # LinkedIn geo ID for Brooklyn
            f"&origin=FACETED_SEARCH"
        )
        urls.append({
            "label": f"People: {title} + payroll in Brooklyn",
            "url": url,
            "type": "people",
            "note": "Look for owners/partners at small firms. Check About section for payroll mentions.",
        })

    return urls


def generate_sales_navigator_queries() -> list[str]:
    """
    Sales Navigator account search query strings.
    Paste these into the Sales Navigator search bar.
    """
    queries = [
        'Industry:"Accounting" Geography:"Brooklyn, New York" Headcount:"1-10" Founded:"2015 to Present"',
        'Industry:"Financial Services" Keywords:"payroll" Geography:"Brooklyn, New York" Headcount:"1-10"',
        'Industry:"Accounting" Keywords:"Gusto OR QuickBooks OR Paychex" Geography:"Brooklyn, New York"',
        'Industry:"Accounting" Keywords:"bookkeeping payroll" Geography:"Brooklyn, New York" Founded:"2015 to Present"',
    ]
    return queries


def generate_competitor_flag_searches() -> list[dict]:
    """
    Searches designed to find firms that mention competitors in their profile.
    These are warm leads — they're actively processing payroll with a named tool.
    """
    urls = []
    base = "https://www.linkedin.com/search/results/companies/"
    for competitor in ["Gusto", "Paychex", "QuickBooks Payroll", "AMS payroll"]:
        query = f"{competitor} Brooklyn accounting"
        url = f"{base}?keywords={query.replace(' ', '%20')}"
        urls.append({
            "label": f"Competitor signal: {competitor}",
            "url": url,
            "type": "competitor_flag",
            "note": f"Firms that mention {competitor} are actively doing payroll — high priority.",
        })
    return urls


def print_linkedin_guide():
    """Print a formatted prospecting guide to stdout."""
    company_urls = generate_company_search_urls()
    people_urls = generate_people_search_urls()
    snav_queries = generate_sales_navigator_queries()
    competitor_urls = generate_competitor_flag_searches()

    lines = []
    lines.append("=" * 70)
    lines.append("LINKEDIN PROSPECTING GUIDE — BROOKLYN ACCOUNTING/PAYROLL FIRMS")
    lines.append("=" * 70)
    lines.append("")
    lines.append("REQUIREMENTS:")
    lines.append("  - Must be logged into LinkedIn")
    lines.append("  - Sales Navigator queries require a Sales Navigator license")
    lines.append("  - Export manually to CSV using the template in output/linkedin_manual_template.csv")
    lines.append("")

    lines.append("─" * 70)
    lines.append("1. STANDARD COMPANY SEARCHES (no Sales Nav needed)")
    lines.append("─" * 70)
    lines.append("When reviewing results, filter by:")
    lines.append("  • Company size: 1–10 employees")
    lines.append("  • Industry: Accounting")
    lines.append("  • Flag any company description mentioning: payroll, Gusto,")
    lines.append("    QuickBooks, Paychex, AMS, Heartland")
    lines.append("")
    for i, item in enumerate(company_urls[:12], 1):  # Show first 12
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append("")

    lines.append("─" * 70)
    lines.append("2. PEOPLE SEARCHES (find decision-makers directly)")
    lines.append("─" * 70)
    for i, item in enumerate(people_urls, 1):
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append(f"       NOTE: {item['note']}")
        lines.append("")

    lines.append("─" * 70)
    lines.append("3. SALES NAVIGATOR QUERIES (copy/paste into Sales Nav search)")
    lines.append("─" * 70)
    for i, q in enumerate(snav_queries, 1):
        lines.append(f"  [{i}] {q}")
        lines.append("")

    lines.append("─" * 70)
    lines.append("4. COMPETITOR SIGNAL SEARCHES (highest priority leads)")
    lines.append("─" * 70)
    lines.append("These firms are already doing payroll with a named competitor.")
    lines.append("They're your warmest leads for a switch pitch.")
    lines.append("")
    for i, item in enumerate(competitor_urls, 1):
        lines.append(f"  [{i}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append(f"       NOTE: {item['note']}")
        lines.append("")

    lines.append("─" * 70)
    lines.append("5. MANUAL ENTRY TEMPLATE")
    lines.append("─" * 70)
    lines.append("  → See: output/linkedin_manual_template.csv")
    lines.append("  Columns: Name, LinkedIn URL, Firm Name, City, Employee Count,")
    lines.append("           Founded Year, Payroll Mentioned, Competitor Detected,")
    lines.append("           Email (if shown), Notes")
    lines.append("")

    guide = "\n".join(lines)
    print(guide)
    return guide


def get_all_linkedin_data() -> dict:
    return {
        "company_searches": generate_company_search_urls(),
        "people_searches": generate_people_search_urls(),
        "sales_navigator_queries": generate_sales_navigator_queries(),
        "competitor_searches": generate_competitor_flag_searches(),
    }
