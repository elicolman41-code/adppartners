# ADP Brooklyn Prospecting System

A four-module system for finding, scoring, and outreaching to Brooklyn-based accounting firms and bookkeepers who process payroll in-house.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API keys
cp config/.env.example config/.env
# Edit config/.env — add your Google Maps and Yelp API keys

# 3. Run everything
python src/main.py

# Run faster (skip website scoring)
python src/main.py --skip-scoring

# Skip specific scrapers
python src/main.py --skip-google --skip-yelp   # DOS + NYSSCPA only

# Load existing leads from CSV (skip scraping, just score + export)
python src/main.py --input-csv output/master_leads.csv --skip-scoring
```

---

## What It Does

### Module 1 — Lead Discovery

| Source | Method | Notes |
|--------|--------|-------|
| Google Maps | Places API (automated) | Requires `GOOGLE_MAPS_API_KEY` |
| Yelp | Fusion API (automated) | Requires `YELP_API_KEY` |
| NYC Dept. of State | HTTP scraper (automated) | No key needed — public data |
| NYSSCPA | API attempt + manual guide | See `output/nysscpa_guide.txt` |
| LinkedIn | Search URL generator | See `output/linkedin_guide.txt` |
| IRS PTIN | Manual guide + Selenium skeleton | See `output/irs_ptin_guide.txt` |

All sources are deduplicated by phone number, domain, and fuzzy name match.

### Module 2 — Website Scoring

Visits each lead's website and scores 1–10:

| Signal | Points |
|--------|--------|
| Payroll mentioned on site | 3 |
| Competitor named (Gusto, Paychex, etc.) | 2 |
| 3+ services listed | 1 |
| Contact page present | 1 |
| Founded after 2015 | 1 |
| 2–10 employees | 1 |
| 10+ reviews | 1 |

- **Score 7–10 → Priority A** (Grid/buyout pitch)
- **Score 4–6 → Priority B** (Revenue share pitch)
- **Score 1–3 → Priority C** (Cold/curiosity email)

### Module 3 — Outreach Sequences

Three email tracks auto-assigned based on priority:

**Track 1 (Priority A) — Grid/Buyout:**
- Day 1: Curiosity email (3 subject variants)
- Day 3: LinkedIn DM / text
- Day 7: Follow-up with $40–80k social proof
- Day 14: Breakup email

**Track 2 (Priority B) — Revenue Share:**
- Day 1: Passive income framing
- Day 3: LinkedIn DM with $10–30k/year anchor
- Day 7: Full program explanation + one-pager offer
- Day 14: Soft breakup

**Track 3 (Priority C) — Cold:**
- Day 1: Single email asking if they do payroll (qualifies them)

All emails: plain language, no buzzwords, short paragraphs, personalized with `[First Name]`, `[Firm Name]`, `[Neighborhood]`.

### Module 4 — Output Files

| File | Contents |
|------|---------|
| `output/master_leads.csv` | All leads, all fields, sorted by score |
| `output/priority_a_leads.csv` | Hot leads only |
| `output/outreach_sequences.csv` | One row per email step per lead |
| `output/salesforce_import.csv` | Salesforce-compatible column names |
| `output/linkedin_manual_template.csv` | Blank template for manual LinkedIn entries |
| `output/linkedin_guide.txt` | All LinkedIn search URLs + Sales Navigator queries |
| `output/irs_ptin_guide.txt` | Step-by-step IRS PTIN directory guide |
| `output/nysscpa_guide.txt` | NYSSCPA manual search guide |
| `output/run_summary.txt` | Stats: total leads, by source, by priority |

---

## Getting API Keys

**Google Maps Places API** (free up to $200/month usage):
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable "Places API"
3. Create credentials → API Key
4. Add to `config/.env` as `GOOGLE_MAPS_API_KEY`

**Yelp Fusion API** (free tier: 500 calls/day):
1. Go to [Yelp Developers](https://www.yelp.com/developers/v3/manage_app)
2. Create an app
3. Copy your API Key
4. Add to `config/.env` as `YELP_API_KEY`

---

## Estimated API Usage

| Source | Calls | Est. Cost |
|--------|-------|-----------|
| Google Maps (51 ZIPs × 8 terms × ~3 pages) | ~1,500–2,000 | ~$3–8 |
| Google Maps Details (per unique place) | ~500–1,500 | ~$5–15 |
| Yelp (51 ZIPs × 8 terms) | ~400 | Free |

---

## LinkedIn Prospecting

Because LinkedIn doesn't offer a public company search API, `output/linkedin_guide.txt` contains:
- 96 ready-to-open company search URLs (by neighborhood + keyword)
- 7 people search URLs (by title + payroll)
- 4 Sales Navigator query strings (copy/paste)
- 4 competitor signal searches (firms mentioning Gusto, Paychex, etc.)

Manual results go into `output/linkedin_manual_template.csv` and can be re-run through the scorer with `--input-csv`.

---

## IRS PTIN Directory

The IRS Tax Preparer directory requires browser interaction. `output/irs_ptin_guide.txt` walks you through each Brooklyn ZIP code and includes a Selenium automation skeleton if you want to automate it.

---

## Re-running with Manual Data

After completing LinkedIn and IRS manual searches, merge your entries into `output/master_leads.csv` and re-run scoring:

```bash
python src/main.py --input-csv output/master_leads.csv
```

---

## File Structure

```
adppartners/
├── config/
│   └── .env.example        ← Copy to .env, add API keys
├── src/
│   ├── main.py             ← Orchestrator (run this)
│   ├── constants.py        ← ZIP codes, keywords, scoring weights
│   ├── google_maps.py      ← Google Maps Places API
│   ├── yelp_scraper.py     ← Yelp Fusion API
│   ├── nyc_dos_scraper.py  ← NYC Dept. of State scraper
│   ├── nysscpa_scraper.py  ← NYSSCPA directory
│   ├── linkedin_queries.py ← LinkedIn URL generator + guide
│   ├── irs_ptin.py         ← IRS PTIN directory guide
│   ├── deduplicator.py     ← Cross-source deduplication
│   ├── website_scorer.py   ← Website analysis + lead scoring
│   ├── outreach_templates.py ← All 3 email tracks
│   └── exporter.py         ← CSV + text file output
├── output/                 ← All generated files land here
│   └── (generated at runtime)
└── requirements.txt
```
