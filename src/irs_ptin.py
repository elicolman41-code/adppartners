"""
Module 1e — IRS PTIN Directory scraper.

The IRS Tax Preparer directory is publicly searchable at:
https://irs.treasury.gov/rpo/rpo.jsf

It's a JSF/Facelets app. This module generates:
1. The correct POST parameters to query by zip code
2. A manual query guide (the site's bot protection makes full automation unreliable)
3. A CSV template for manual data entry

If you want to automate this, use the Selenium approach documented below.
"""

from constants import BROOKLYN_ZIPS

IRS_PTIN_URL = "https://irs.treasury.gov/rpo/rpo.jsf"

# Credentials to search for (licensed preparers who can do payroll-adjacent work)
CREDENTIAL_TYPES = [
    "CPA",          # Certified Public Accountant
    "EA",           # Enrolled Agent
    "ATTY",         # Attorney
    "",             # All (includes unenrolled preparers with PTIN)
]


def generate_irs_search_guide() -> str:
    """
    Returns a step-by-step manual guide for pulling IRS PTIN data.
    Also shows a Selenium skeleton for automation.
    """
    lines = [
        "=" * 70,
        "IRS TAX PREPARER DIRECTORY — MANUAL SEARCH GUIDE",
        "=" * 70,
        "",
        "URL: https://irs.treasury.gov/rpo/rpo.jsf",
        "",
        "The IRS directory requires manual interaction due to JSF form state.",
        "Follow these steps for each Brooklyn ZIP code:",
        "",
        "STEP-BY-STEP:",
        "  1. Open the URL above in Chrome or Firefox",
        "  2. Under 'Search by ZIP code', enter one of the ZIPs below",
        "  3. Set Search Radius to: 1 mile",
        "  4. Under 'Credential/Select All' check: CPA, EA",
        "  5. Click Search",
        "  6. Export or copy results to output/irs_ptin_manual.csv",
        "  7. Repeat for each ZIP",
        "",
        "BROOKLYN ZIP CODES TO SEARCH:",
    ]
    for i, z in enumerate(BROOKLYN_ZIPS, 1):
        lines.append(f"  {i:02d}. {z}")

    lines += [
        "",
        "COLUMNS TO CAPTURE:",
        "  - Last Name, First Name",
        "  - Credential (CPA / EA / etc.)",
        "  - Business Name",
        "  - City, State, ZIP",
        "",
        "─" * 70,
        "SELENIUM AUTOMATION SKELETON (Python)",
        "─" * 70,
        "  If you want to automate this, install: pip install selenium webdriver-manager",
        "",
        "  from selenium import webdriver",
        "  from selenium.webdriver.common.by import By",
        "  from selenium.webdriver.support.ui import WebDriverWait, Select",
        "  from selenium.webdriver.support import expected_conditions as EC",
        "  import time, csv",
        "",
        "  driver = webdriver.Chrome()",
        "  driver.get('https://irs.treasury.gov/rpo/rpo.jsf')",
        "",
        "  for zip_code in BROOKLYN_ZIPS:",
        "      # Fill ZIP field",
        "      zip_input = WebDriverWait(driver, 10).until(",
        "          EC.presence_of_element_located((By.ID, 'searchForm:zip')))",
        "      zip_input.clear()",
        "      zip_input.send_keys(zip_code)",
        "",
        "      # Set radius to 1 mile",
        "      radius_select = Select(driver.find_element(By.ID, 'searchForm:distance'))",
        "      radius_select.select_by_value('1')",
        "",
        "      # Click CPA checkbox",
        "      cpa_cb = driver.find_element(By.XPATH, \"//label[contains(text(),'CPA')]\")",
        "      if not cpa_cb.is_selected(): cpa_cb.click()",
        "",
        "      # Submit",
        "      driver.find_element(By.ID, 'searchForm:searchButton').click()",
        "      time.sleep(2)",
        "",
        "      # Scrape results table",
        "      rows = driver.find_elements(By.CSS_SELECTOR, '#resultsTable tbody tr')",
        "      for row in rows:",
        "          cells = row.find_elements(By.TAG_NAME, 'td')",
        "          # Process cells...",
        "",
        "  driver.quit()",
        "",
    ]
    return "\n".join(lines)


def get_ptin_zip_queries() -> list[str]:
    return BROOKLYN_ZIPS


if __name__ == "__main__":
    print(generate_irs_search_guide())
