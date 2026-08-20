# Job: Monday Sweep

Trigger fires ~8am ET Mondays into the main session. Fleet: Signal Scout, Registrar, Grid Hunter, Directory Miner, Nationwide Tracker, Trigger Watcher (light) — all Opus, hard cap 7, one round, no loops. Fable does Pipeline Nurse inline.
Scoring: Actionability 25 / Referral 20 / Recency 15 / Grid 10 / Timing 10 / Growth 10 / Proximity-or-Community 10.
Output: update dashboard (artifact + docs/index.html), refresh Top-5, SHORT summary. Update vault firm notes for anything new.

## Signal Scout — MUST route through Firecrawl
Native fetches fail: reddit.com, linkedin.com, trustpilot, gusto.com, quickbooks.intuit.com, proadvisor.intuit.com are all egress-blocked by the proxy. Agent must use `mcp__Firecrawl__firecrawl_search` (server-side, bypasses block) — never fabricate posts when blocked; return empty instead.

Search terms:
- "switching from Gusto" / "leaving Gusto" / "Gusto payroll problems"
- "QuickBooks payroll" + 2026 changes (automated taxes July 1 2026, Desktop Payroll sunset May 31 2026)
- "fired my payroll company" / "payroll company messed up"
- r/Accounting, r/Bookkeeping, r/smallbusiness complaint threads
- CPAs/bookkeepers asking for payroll provider recommendations

Use signals to TIME outreach — never quote someone's post back at them.

## Lusha signals step (already owned, unused)
After scoring, run on top-ranked leads:
- `signals_companies_search` / `signal_score_companies` — buying intent
- `website_visits_search` — firms visiting payroll/HR sites
- `buying_group_search` — decision makers
- `prospecting_contact_enrich` — crack anonymous PLLCs
First run: check `account_usage` + `signals_company_filters` to confirm the plan tier includes intent data.

## Crustdata step (new — pending user connect)
- `crustdata_company_linkedin_posts` — public LinkedIn posts from target firms
- `crustdata_job_search_live` — firms hiring bookkeepers/payroll staff = growth + payroll pain signal
- `crustdata_company_enrich` — headcount/growth on ranked leads

## PENDING (apply when scheduling connector reconnects)
Trigger trig_01KYWKW1yXmM76tmH77AXua6 still needs written in: Nationwide Tracker in fleet (cap→7), Lusha signals step, Firecrawl-routed Signal Scout, Crustdata step.

## Connector status (as of 2026-08-20)
- Firecrawl: connected, flapping — WORKS (verified on M&H research)
- Lusha: flapping, signals tools never tested
- Crustdata: NOT installed — Eli connecting via claude.ai
- Scheduling connector: DOWN — blocking the trigger edits above
