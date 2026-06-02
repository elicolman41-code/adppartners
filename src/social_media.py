"""
Social media research module.

Searches for Brooklyn accounting firms across:
  1. Google Business Profiles (via Maps search URLs + scraping)
  2. Instagram (hashtag and username search URLs)
  3. Facebook (business page and group search URLs)
  4. Nextdoor (neighborhood business recommendations)
  5. LinkedIn (already covered in linkedin_queries.py — see that file)

IMPORTANT: Instagram, Facebook, and Nextdoor do not provide public APIs.
This module generates:
  - Ready-to-open search URLs for manual review
  - A scraping guide using browser DevTools
  - Helper functions to parse any data you paste/export manually

For Google Business Profiles: the module attempts direct search scraping
via the Google Maps search API (if key is set) — this supplements the
Places API data already collected in google_maps.py by looking for
signals in review text and owner responses.
"""

import os
import re
import time
import requests
from urllib.parse import quote_plus
from constants import BROOKLYN_ZIPS, COMPETITOR_KEYWORDS, PAYROLL_KEYWORDS

# ─────────────────────────────────────────────────────────────────────────────
# 1. INSTAGRAM SEARCH
# ─────────────────────────────────────────────────────────────────────────────

INSTAGRAM_HASHTAGS = [
    "brooklynaccountant",
    "brooklyncpa",
    "brooklynbookkeeper",
    "brooklynbusiness",
    "brooklyntax",
    "nycaccountant",
    "nyccpa",
    "nycbookkeeper",
    "smallbusinessbrooklyn",
    "brooklynsmallbusiness",
    "payrollservices",
    "accountingfirm",
    "bookkeepingservices",
    "cpafirm",
    "taxprep",
    "brooklynentrepreneur",
]

INSTAGRAM_SEARCH_TERMS = [
    "brooklyn accountant",
    "brooklyn CPA",
    "brooklyn bookkeeper",
    "brooklyn payroll services",
    "brooklyn tax prep",
]


def generate_instagram_search_urls() -> list[dict]:
    """
    Generate Instagram search and hashtag URLs.
    Instagram requires login to view content.
    """
    urls = []

    # Hashtag pages
    for tag in INSTAGRAM_HASHTAGS:
        urls.append({
            "label": f"Instagram hashtag: #{tag}",
            "url": f"https://www.instagram.com/explore/tags/{tag}/",
            "type": "hashtag",
            "note": "Browse posts; look for firm accounts in profile links",
        })

    # Username search (Instagram has no native keyword search — use Google)
    for term in INSTAGRAM_SEARCH_TERMS:
        google_query = f'site:instagram.com "{term}"'
        urls.append({
            "label": f"Google → Instagram: {term}",
            "url": f"https://www.google.com/search?q={quote_plus(google_query)}",
            "type": "google_to_instagram",
            "note": "Google indexes Instagram profiles. Click through to find firm accounts.",
        })

    return urls


def generate_instagram_dm_approach() -> str:
    return """
INSTAGRAM OUTREACH APPROACH
─────────────────────────────────────────
1. Find the firm's Instagram profile (use URLs above)
2. Check their bio for: phone, website, services listed
3. Look at recent posts — do they mention payroll, tax season, QuickBooks?
4. If they have a business profile, their email is often in the bio
5. DM message template:

   "Hi [First Name], I saw your profile and noticed you work with payroll
   clients in Brooklyn. I work with a few firms in the area on a program
   that's been generating some meaningful extra income — and in some cases,
   a one-time payout. Would a quick 10-minute call make sense?"

WHAT TO CAPTURE per Instagram profile:
  - Handle (@username)
  - Full name / firm name
  - Bio text (screenshot it)
  - Phone number (if listed)
  - Website link
  - Email (if listed under "Contact")
  - Follower count (proxy for firm size/activity)
  - Last post date (is this firm active?)

RECORD TO: output/instagram_manual.csv (see template)
"""


# ─────────────────────────────────────────────────────────────────────────────
# 2. FACEBOOK SEARCH
# ─────────────────────────────────────────────────────────────────────────────

FACEBOOK_GROUPS_KEYWORDS = [
    "Brooklyn business owners",
    "Brooklyn small business",
    "Brooklyn entrepreneurs",
    "Brooklyn networking",
    "NYC accountants",
    "NYC bookkeepers",
    "Brooklyn Chamber of Commerce",
]


def generate_facebook_search_urls() -> list[dict]:
    urls = []

    # Facebook business page search
    fb_terms = [
        "accountant brooklyn",
        "CPA brooklyn",
        "bookkeeper brooklyn",
        "payroll services brooklyn",
        "tax preparer brooklyn",
        "accounting firm brooklyn",
    ]
    for term in fb_terms:
        urls.append({
            "label": f"Facebook Pages: {term}",
            "url": f"https://www.facebook.com/search/pages/?q={quote_plus(term)}",
            "type": "facebook_pages",
            "note": "Filter to Pages. Look for About section — phone, website, services. Check if they mention payroll.",
        })

    # Facebook Groups (members are your prospects)
    for group_kw in FACEBOOK_GROUPS_KEYWORDS:
        urls.append({
            "label": f"Facebook Group: {group_kw}",
            "url": f"https://www.facebook.com/search/groups/?q={quote_plus(group_kw)}",
            "type": "facebook_groups",
            "note": (
                "Join the group. Look for accountants/bookkeepers answering questions. "
                "They're advertising themselves — reach out directly."
            ),
        })

    # Google → Facebook (no login required)
    for term in ["brooklyn accountant", "brooklyn CPA payroll", "brooklyn bookkeeper"]:
        urls.append({
            "label": f"Google → Facebook: {term}",
            "url": f"https://www.google.com/search?q={quote_plus('site:facebook.com ' + term)}",
            "type": "google_to_facebook",
            "note": "No login needed. Google indexes public Facebook pages.",
        })

    return urls


def generate_facebook_approach() -> str:
    return """
FACEBOOK OUTREACH APPROACH
─────────────────────────────────────────
HIGH-VALUE TACTIC — Brooklyn Business Groups:

1. Join: "Brooklyn Small Business Owners", "Brooklyn Entrepreneurs",
   "NYC Accountants Network", local Chamber of Commerce groups

2. Search within the group for: "payroll", "bookkeeping", "CPA", "accountant"
   — You'll find posts from business owners ASKING for recommendations
   — You'll find accountants ANSWERING and promoting themselves

3. When you find an accountant active in a group:
   a. Look at their personal or business page
   b. Check the About section for phone, website, email
   c. See what services they list / whether payroll is mentioned

4. DM approach (Facebook Messenger):
   "Hi [Name], I found your page through the Brooklyn Business Owners group.
   I work with accounting firms in Brooklyn on a program that's helped a few
   firms here turn their payroll clients into a meaningful income stream.
   Would it be worth a 10-minute call?"

KEY FACEBOOK DATA TO CAPTURE:
  - Page name
  - Website URL
  - Phone (often in About section)
  - Services listed
  - Review count + rating
  - Last post date
  - Whether payroll is mentioned anywhere

RECORD TO: output/facebook_manual.csv
"""


# ─────────────────────────────────────────────────────────────────────────────
# 3. GOOGLE BUSINESS PROFILES — REVIEW MINING
# ─────────────────────────────────────────────────────────────────────────────

def generate_google_business_search_urls() -> list[dict]:
    """
    Generate Google Maps search URLs for finding accounting firms by neighborhood.
    These go to the Google Maps web UI — no API key needed.
    Useful for checking reviews and owner responses for payroll signals.
    """
    neighborhoods = [
        ("Williamsburg", "11211"),
        ("Park Slope", "11215"),
        ("Bay Ridge", "11209"),
        ("Crown Heights", "11213"),
        ("Bushwick", "11221"),
        ("Sunset Park", "11220"),
        ("Flatbush", "11226"),
        ("DUMBO Downtown Brooklyn", "11201"),
        ("Borough Park", "11219"),
        ("Bensonhurst", "11214"),
        ("Sheepshead Bay", "11235"),
        ("Midwood", "11230"),
        ("Bed-Stuy", "11233"),
        ("Greenpoint", "11222"),
        ("Carroll Gardens", "11231"),
    ]

    search_terms = ["accountant", "CPA", "bookkeeper", "payroll services", "tax preparer"]
    urls = []

    for neighborhood, zip_code in neighborhoods:
        for term in search_terms:
            query = f"{term} {neighborhood} Brooklyn NY"
            url = f"https://www.google.com/maps/search/{quote_plus(query)}/"
            urls.append({
                "label": f"Google Maps: {term} in {neighborhood}",
                "url": url,
                "zip": zip_code,
                "type": "google_maps_manual",
                "note": (
                    "Scan listing cards. Click 'More reviews' and search within reviews "
                    "for 'payroll'. Owner responses mentioning payroll = strong signal."
                ),
            })

    return urls


def generate_review_mining_guide() -> str:
    return """
GOOGLE BUSINESS PROFILE — REVIEW MINING GUIDE
─────────────────────────────────────────────────────────
This is one of the highest-signal research tactics available without API access.
Reviews and owner responses often explicitly mention payroll services.

WHAT TO LOOK FOR IN REVIEWS:
  • "they handle our payroll" → confirmed payroll client
  • "QuickBooks payroll setup" → competitor detected
  • "switched from Gusto" → competitor + switcher mentality
  • "payroll taxes" / "941" / "W-2" → active payroll processing
  • "highly recommend for payroll" → business owner testimonial

WHAT TO LOOK FOR IN OWNER RESPONSES:
  • "we offer full-service payroll" → confirmed payroll service
  • "our payroll team" → has dedicated payroll staff
  • Any competitor brand name mentioned

HOW TO MINE EFFICIENTLY (10 minutes per neighborhood):
  1. Open Google Maps URL for the neighborhood
  2. Click the first 3–5 accounting/CPA listings
  3. Click "Reviews" tab → Ctrl+F → search "payroll"
  4. If found, note: firm name, phone, website, # payroll reviews
  5. Check Google Business Profile for: hours, employees listed, founded date

BROWSER AUTOMATION OPTION (if you want to batch this):
  Use browser DevTools → Console → paste this snippet on a Google Maps results page:
  ─────────────────────────────────────────────────────────
  // Extracts visible listing names + ratings from Google Maps results panel
  [...document.querySelectorAll('[role="feed"] .fontHeadlineSmall')].map(el => el.textContent)
  ─────────────────────────────────────────────────────────
  This gives you all firm names on the current page instantly.

RECORD TO: output/google_manual.csv
"""


# ─────────────────────────────────────────────────────────────────────────────
# 4. NEXTDOOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_nextdoor_approach() -> str:
    return """
NEXTDOOR PROSPECTING APPROACH
─────────────────────────────────────────
Nextdoor is underused for B2B prospecting but it's highly valuable in Brooklyn
because small business owners frequently ask neighbors for accountant/bookkeeper
recommendations — and local accountants reply to promote themselves.

URL: https://nextdoor.com

1. CREATE A FREE PERSONAL ACCOUNT if you don't have one
   - Use your Brooklyn address (or a Brooklyn ZIP code)

2. SEARCH WITHIN NEXTDOOR:
   - Search: "accountant", "bookkeeper", "CPA", "payroll", "tax"
   - Filter to: "Posts" and "Recommendations"

3. WHAT YOU'RE LOOKING FOR:
   - Posts by business owners asking "who does payroll for small businesses?"
   - Replies by local accountants self-promoting
   - "Business" profile listings in the Neighborhood Favorites section

4. WHAT TO CAPTURE per lead:
   - First and last name of the accountant
   - Firm name (if mentioned)
   - Phone number (sometimes in replies)
   - Website (sometimes linked)
   - Neighborhood they serve

5. OUTREACH:
   Nextdoor has a direct message feature. Keep it ultra-local:
   "Hi [Name], I found your recommendation in the [neighborhood] Nextdoor
   group. I work with accounting firms in Brooklyn on a program that's been
   generating real income for firms like yours. Would you be open to a
   10-minute call?"

RECORD TO: output/nextdoor_manual.csv
"""


# ─────────────────────────────────────────────────────────────────────────────
# 5. YELP REVIEWS — COMPETITOR SIGNAL MINING
# ─────────────────────────────────────────────────────────────────────────────

def generate_yelp_review_mining_urls() -> list[dict]:
    """
    Direct Yelp search URLs for Brooklyn accounting firms.
    Yelp reviews frequently mention specific payroll software.
    """
    categories = ["accountants", "bookkeepers", "payrollservices", "taxservices"]
    neighborhoods = ["Brooklyn", "Williamsburg, Brooklyn", "Park Slope, Brooklyn",
                     "Bay Ridge, Brooklyn", "Flatbush, Brooklyn", "Crown Heights, Brooklyn"]
    urls = []

    for neighborhood in neighborhoods:
        for category in categories[:2]:  # accountants + bookkeepers = highest value
            url = (
                f"https://www.yelp.com/search?"
                f"find_desc={quote_plus(category.replace('s', ''))}&"
                f"find_loc={quote_plus(neighborhood + ', NY')}"
            )
            urls.append({
                "label": f"Yelp: {category} in {neighborhood}",
                "url": url,
                "type": "yelp_manual",
                "note": "Click each listing → Reviews → search for 'payroll', 'Gusto', 'QuickBooks'",
            })

    return urls


# ─────────────────────────────────────────────────────────────────────────────
# 6. OUTPUT GENERATOR
# ─────────────────────────────────────────────────────────────────────────────

def generate_social_media_report(output_dir: str = "output") -> str:
    """
    Write a comprehensive social media prospecting guide to a text file.
    Returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "social_media_prospecting_guide.txt")

    ig_urls = generate_instagram_search_urls()
    fb_urls = generate_facebook_search_urls()
    gmaps_urls = generate_google_business_search_urls()
    yelp_urls = generate_yelp_review_mining_urls()

    lines = [
        "=" * 70,
        "SOCIAL MEDIA PROSPECTING GUIDE — BROOKLYN ACCOUNTING/PAYROLL FIRMS",
        "=" * 70,
        "",
        "This guide covers 5 platforms: Instagram, Facebook, Google Business",
        "Profiles, Nextdoor, and Yelp. Each has different signals and tactics.",
        "",
        "PRIORITY ORDER (based on signal quality):",
        "  1. Google Business Profiles — review mining for payroll mentions",
        "  2. Facebook Groups — self-promoting accountants in business groups",
        "  3. Yelp Reviews — competitor software mentions",
        "  4. Instagram — secondary; best for younger/tech-forward firms",
        "  5. Nextdoor — niche but highly local; small but warm leads",
        "",
    ]

    # Google Maps
    lines += [
        "─" * 70,
        "1. GOOGLE BUSINESS PROFILES (highest signal)",
        "─" * 70,
        generate_review_mining_guide(),
        "",
        "SEARCH URLS BY NEIGHBORHOOD:",
        "",
    ]
    for i, item in enumerate(gmaps_urls[:20], 1):  # First 20
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append("")

    # Facebook
    lines += [
        "─" * 70,
        "2. FACEBOOK PAGES & GROUPS",
        "─" * 70,
        generate_facebook_approach(),
        "",
        "SEARCH URLS:",
        "",
    ]
    for i, item in enumerate(fb_urls, 1):
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append(f"       NOTE: {item['note']}")
        lines.append("")

    # Yelp
    lines += [
        "─" * 70,
        "3. YELP REVIEW MINING",
        "─" * 70,
        "  Yelp reviewers frequently name specific software ('they use Gusto',",
        "  'great with QuickBooks payroll'). These are warm signals.",
        "",
        "SEARCH URLS:",
        "",
    ]
    for i, item in enumerate(yelp_urls, 1):
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append("")

    # Instagram
    lines += [
        "─" * 70,
        "4. INSTAGRAM",
        "─" * 70,
        generate_instagram_dm_approach(),
        "",
        "HASHTAG + SEARCH URLS:",
        "",
    ]
    for i, item in enumerate(ig_urls[:20], 1):
        lines.append(f"  [{i:02d}] {item['label']}")
        lines.append(f"       {item['url']}")
        lines.append("")

    # Nextdoor
    lines += [
        "─" * 70,
        "5. NEXTDOOR",
        "─" * 70,
        generate_nextdoor_approach(),
    ]

    # Manual CSV templates note
    lines += [
        "",
        "─" * 70,
        "MANUAL ENTRY TEMPLATES",
        "─" * 70,
        "  All social media leads should be entered into:",
        "  → output/social_media_manual.csv",
        "",
        "  Then run: python src/main.py --input-csv output/social_media_manual.csv",
        "  This will score them and merge them into your master list.",
        "",
    ]

    content = "\n".join(lines)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[Social Media] Guide written to {path}")
    return path


def get_all_social_urls() -> dict:
    return {
        "instagram": generate_instagram_search_urls(),
        "facebook": generate_facebook_search_urls(),
        "google_maps": generate_google_business_search_urls(),
        "yelp": generate_yelp_review_mining_urls(),
    }
