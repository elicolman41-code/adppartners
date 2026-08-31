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

## 🔑 CHANNEL BREAKTHROUGH 2026-08-24 — DayOneLead
**dayonelead.com republishes NY Division of Corporations filings** by borough + industry WITH REAL FILING DATES. This solves the recency problem that has crippled the new-firm lane since day one (NY DOS's own search is a POST form, unqueryable).
- EGRESS-BLOCKED for our tools. **ELI must open it manually** — ~10 min:
  - dayonelead.com/new-york/brooklyn/bookkeeping (5 entities)
  - dayonelead.com/new-york/brooklyn/accounting (19 entities)
  - dayonelead.com/new-york/bronx/tax-preparation (6 entities)
- Site claims it carries owner names + contact info behind a trial.
- ~30 DOS-verified new firms sitting there.

## RETIRED TECHNIQUE
**Yelp "was founded in 20XX" search — DEAD.** That phrase lives in page body text the search index does not expose. It never worked and never could through search. Stop spending calls on it.

## ENRICHMENT PATH for the 3 verified new formations
PTIN Directory (ptindirectory.com) searched by ZIP 11219 (SA Bookkeeping) and 11235 (Atlantik) should attach preparer names + phones.

## NEIGHBORHOODS THAT RETURNED NOTHING via keyword search
Bay Ridge, Bensonhurst, Sheepshead Bay, Coney Island, Crown Heights, Bed-Stuy, East New York, Flushing, Woodside, Astoria, Elmhurst, Soundview, Port Richmond. Keyword search surfaces national chains + mobile-notary SEO pages there. These need a DIRECTORY-PAGE pass (Yelp/YellowPages listing pages opened directly), which requires scrape access.

## DEAD
Unlimited Multi Service (994 Broadway, Bushwick) — CLOSED, confirmed Yelp. Left on board at score 0 so it is not re-surfaced as a new find.

## Sweep 2026-08-24 (rerun) — method finding that MATTERS
**Keyword searches return SEO doorway pages. DIRECTORY-RECORD searches return real firms with phones.**
Go at Yelp/YellowPages/Manta/TaxBuzz/PTIN/BBB/Yahoo Local BUSINESS-DETAIL pages, not category keyword queries. This one change took a neighborhood set that produced ZERO last run to 10 callable leads.

## ⚠️ EGRESS REGRESSION
directory.relayfi.com was reachable earlier today, now BLOCKED. Also blocked: xero.com, most firm domains. Firecrawl is SEARCH-ONLY (no scrape tool exists).
=> Directory Miner returned 0 callable this run. Not an effort problem.
**accountants.ramp.com IS reachable** and is untouched — point the next directory pass there first.

## STILL UNCOVERED (need directory-record passes)
- Brooklyn: Canarsie, Flatlands, Mill Basin, Gravesend, Prospect Heights, Sunset Park north, Brownsville proper
- Bronx: Fordham, Kingsbridge, Riverdale, Throgs Neck, Soundview, Hunts Point, Mott Haven, Pelham Bay (Bronx yielded only 2 firms total — dominated by H&R Block SEO pages)
- Staten Island: entire NORTH SHORE (St. George, Port Richmond, Great Kills, Tottenville)
- Queens: Sunnyside, Ridgewood, Elmhurst, Corona, Bayside, Whitestone, Far Rockaway, Rego Park, Ozone Park

## CHASE FIRST NEXT RUN
**Tax & Financial Services (Bay Ridge)** — explicitly advertises helping clients INCORPORATE, open LLCs, C Corps and S Corps; est. 1980. Best profile match found all sweep. Agent ran out of budget before landing the phone. https://www.yelp.com/biz/tax-and-financial-services-brooklyn
Also name-only: Bay Ridge Tax Planning (9710 3rd Ave), Easy Tax Services (3094 Coney Island Ave), Schwartz Accounting (1839 Flatbush Ave), Maria Agency (590 Manhattan Ave, Greenpoint).

## CONFIRMED CLOSED — do not call
- Unlimited Multi Service, 994 Broadway Bushwick (Yelp, July 2026)
- Astoria Tax Service, 45-18 Court Sq (Yelp)

## NAME COLLISION WARNING
**ASR Accounting & Tax (Bronx, 2718 Lurting Ave)** is a NEW lead and is NOT Aldo's ASR Consulting on the daily to-do. Different firms.

## Sweep 2026-08-31 — method status
**WORKING:**
- **Gusto partner directory** — fully readable, publishes CLIENT COUNTS + partner-since years. Now the workhorse. Lead with it.
- **DayOneLead via WebSearch allowed_domains** — still works but PARTIAL. Resolved: /brooklyn/bookkeeping, /brooklyn/business-consulting, /manhattan/tax-preparation. FAILED to resolve as category pages: /queens/accounting, /brooklyn/tax-preparation, /manhattan/accounting (summarizer redirected to Bronx or to entity pages).
- **bizprofile.net — NEW, add to Stage 2 rotation ahead of ZoomInfo.** Returns exact DOS filing dates AND document numbers for entities DayOneLead won't date.

**DEGRADED:**
- **accountants.ramp.com is now EGRESS-BLOCKED** (was reachable Aug 24). Names leak via WebSearch snippets only. Second directory to degrade after Relay.
- bill.com/find-an-accountant reachable but results skew national; won't filter to Brooklyn.

**CAUTION on Gusto client counts:** they are GUSTO clients, not the firm's total book. Never quote the number back to a prospect as their client count.

## TALKING-POINT CORRECTION (Intuit ProAdvisor → ProPartner)
Existing **30% ProAdvisor Preferred Pricing discounts and revenue share are GRANDFATHERED** for subscriptions set up before launch. **Do NOT tell CPAs they lose their discount — that is wrong and they will know it.**
Real hooks instead: QBOA discontinued Dec 2026 (firms move to a free Core plan); **Accelerate goes to $149/mo on Jan 20 2027**; Books Close $8/client/mo (≤50 clients), $6 (>50); ProAdvisor tiers sunset early 2027.

## NY DFS 2027 SMALL GROUP — STILL NO RULING as of Aug 31 2026
Most recent DFS rate-decision press release is still the 2026 one (Aug 29 2025). 2027 filings remain listed as requested/proposed: ~25.3% (ACA Signups tally) / 25.7% (DFS weighted). **Collateral is fine — it already says "requested." Never say "approved."**
For 2026 DFS cut small group 24% requested → 13% approved (45.8% cut). **RE-CHECK WEDNESDAY**, not next Monday — the ruling is overdue.

## QUEENS PROBLEM
No Queens firm cleared verification this run. Every Queens-titled result traced to a templated geo-SEO page or an office physically in Brooklyn/Bronx. Next Queens attempt must work from a Queens ZIP-anchored directory, not search titles.
