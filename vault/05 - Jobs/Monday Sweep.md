# Job: Monday Sweep

Trigger fires ~8am ET Mondays into the main session. Fleet: Signal Scout, Registrar, Grid Hunter, Directory Miner, Trigger Watcher (light) — all Opus, hard cap 5, one round, no loops.
**NATIONWIDE TRACKER REMOVED 2026-08-24** (Eli's call). NYC only. Its 13 leads were also stripped from the dashboard — they were padding the 80+ tier (call-now count went 15 -> 6 once removed, revealing the NYC board is much thinner than headline numbers suggested). Fable does Pipeline Nurse inline.
Scoring: Actionability 25 / Referral 20 / Recency 15 / Grid 10 / Timing 10 / Growth 10 / Brooklyn proximity 10.
**Weight ACTIONABILITY hardest.** 13 board leads are tagged 'crack' (no phone/email) = not callable. Callable beats interesting.
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
Trigger trig_01KYWKW1yXmM76tmH77AXua6 still needs written in: REMOVE Nationwide Tracker (cap→5), remove the claude.ai artifact republish step (Eli: no artifacts — deliver downloads/*.html instead), Lusha signals step, Firecrawl-routed Signal Scout, Crustdata step.
Also: STAGGER Firecrawl-dependent agents — concurrent agents 429 each other.

## Connector status (as of 2026-08-20)
- Firecrawl: connected, flapping — WORKS (verified on M&H research)
- Lusha: flapping, signals tools never tested
- Crustdata: NOT installed — Eli connecting via claude.ai
- Scheduling connector: DOWN — blocking the trigger edits above
