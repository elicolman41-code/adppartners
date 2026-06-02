"""Shared constants for the ADP Brooklyn prospecting system."""

BROOKLYN_ZIPS = [
    "11201", "11202", "11203", "11204", "11205", "11206", "11207", "11208",
    "11209", "11210", "11211", "11212", "11213", "11214", "11215", "11216",
    "11217", "11218", "11219", "11220", "11221", "11222", "11223", "11224",
    "11225", "11226", "11228", "11229", "11230", "11231", "11232", "11233",
    "11234", "11235", "11236", "11237", "11238", "11239", "11241", "11242",
    "11243", "11244", "11245", "11247", "11248", "11249", "11251", "11252",
    "11254", "11255", "11256",
]

SEARCH_TERMS = [
    "accountant",
    "bookkeeper",
    "CPA",
    "certified public accountant",
    "payroll services",
    "tax preparer",
    "accounting firm",
    "bookkeeping services",
]

COMPETITOR_KEYWORDS = [
    "paychex", "gusto", "quickbooks", "quickbooks payroll", "qbo payroll",
    "ams", "heartland", "rippling", "justworks", "adp", "run by adp",
    "intuit payroll", "square payroll", "onpay", "zenefits",
]

PAYROLL_KEYWORDS = [
    "payroll", "payroll processing", "payroll services", "payroll management",
    "payroll administration", "direct deposit", "941", "w-2", "w2",
    "1099", "wage", "paycheck", "payroll tax",
]

NYC_DOS_SEARCH_TERMS = [
    "accounting", "bookkeeping", "payroll", "tax", "cpa", "bookkeeper",
]

# Priority scoring weights
SCORE_WEIGHTS = {
    "payroll_mentioned": 3,
    "competitor_named": 2,
    "multiple_services": 1,
    "contact_page": 1,
    "founded_after_2015": 1,
    "employee_count_2_10": 1,
    "review_count_over_10": 1,
}

OUTPUT_DIR = "output"
