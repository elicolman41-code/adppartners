# Social Signal Findings — first live sweep (2026-08-20)

Ran via Firecrawl (reddit egress-blocked natively; Firecrawl bypasses). ~6 credits.

## KEY: prospects' own words for the rev-share pitch
r/Accounting, "Need Help Finding an Alternative to Quickbooks for Payroll" — top answer:
> "What she's looking for has an industry term — it's often called **accountant partner or wholesale payroll**. The idea is that **the accountant owns the client**."

USE THIS LANGUAGE in outreach. Beats "partner program" (reads as vendor-speak).

## Live displacement intent (last 3 mo)
- r/Payroll "Best QBO integration?" — "bad service from QB desktop assisted payroll... want to move away from Intuit for payroll taxes, forms"
- r/Bookkeeping "Why does everyone recommend Gusto for payroll?" — Gusto support complaints
- r/quickbooksonline "Stay Away from Quickbooks Online"
- r/Accounting "Bookkeeping and payroll software recommendation" — weighing gusto/adp by name
- r/Payroll "PLEASE HELP FIND PAYROLL PROVIDER"

## Slava pattern is common, not unique
r/Bookkeeping: bookkeeper asked to run client weekly payroll in QBO on a $250 engagement "should be $350+".
=> "get paid on the payroll you already do" is a repeatable pitch, not a one-off.

## Gusto pain cluster (Capterra verified reviews)
- 941 misfilings, missed payments
- Slow support; upper-tier support doesn't understand payroll tax
- **Cannot handle an employee working in two states** — reviewer flagged this as common in the Northeast. STRONG tri-state wedge.
- Paychex is AICPA/CPA.com preferred provider — that's the CPA-channel competitor.

## LIMITATION — do not over-invest here
Reddit posters are pseudonymous. No names, no firms. NYC/Brooklyn geo-targeted searches returned only career/COL threads — people don't post their city.
=> Social listening = MESSAGE INTEL + TIMING, not named leads. Named leads still come from NY DOS, NYSED, Gusto partner directory.

## Connector status
- Firecrawl: WORKS. Only tool that reaches reddit.
- Lusha: **FREE plan, 40 credits total.** Signals work but 1 credit/company; phone reveal = 5. Not viable for recurring sweeps. Reserve for cracking specific anonymous PLLCs. Upgrade or don't build the sweep on it.
- Crustdata: installed, server NOT connecting, no tools loaded. Was the best shot at named leads (LinkedIn posts + bookkeeper job postings). Eli to check API key registered on Crustdata side.

---

# Sweep 2 — 2026-08-20 (manual run, 5 agents)

## NEW: Intuit's real 2026 wound is CONTROL, not price
QBO mandatory automated payroll taxes (July 1 2026). Accountants are angrier than owners. Their words:
- "we will no longer be able to decide WHEN we pay (or if we do pay) our payroll taxes" (r/QuickBooks)
- "QBO payroll taxes will no longer give us the option of manually entering payroll tax payments. It will withdraw the money from the accounts" (r/quickbooksonline)
- "Anyone else get the email starting June 30th you can no longer turn off automated payments or filing?" (r/Bookkeeping)
- "the system defaults to aggressive prepayment schedules rather than holding funds" (r/QuickBooks, "screwed up automatic payroll taxes on day 1")
- ~~"Intuit charges ~$50/mo to OPT OUT"~~ **RETRACTED 2026-08-24.** Came from a Reddit thread TITLE only. UNVERIFIABLE — no authoritative source documents any paid opt-out. Reality: as of July 1 2026 the toggle is simply GONE for all users (mandatory since Nov 15 2025 for new accounts). DO NOT SAY THIS TO A CPA.

=> LEAD WITH: who controls the debit date and the impound. NOT price.
=> For a CPA: their client's cash gets pulled early, and the CPA owns that relationship damage, not Intuit.

## NEW competitor weaknesses
- **TriNet**: "did not file our MA state taxes for almost two years. Withheld all the money for it, did not file" (r/humanresources — OLD thread, verify before repeating)
- **Insperity**: "extremely slow customer support, tickets taking months" — and ADP TotalSource already in that buyer's consideration set (r/nonprofit)
- **Wave Payroll**: silent backend migration to third-party, "incorrect data, missing records" — NEW displacement source, not previously tracked

## ⚠️ ALL QUOTES ARE SEARCH SNIPPETS, NOT VERIFIED FULL QUOTES
Agent never opened a thread (Firecrawl 429). Truncated mid-sentence, no confirmed dates. OPEN THE THREAD before any prospect-facing use.

## INFRASTRUCTURE FINDINGS (fix before next sweep)
1. **Firecrawl 429s throttled 3 of 5 agents.** Running 5 concurrent agents against one Firecrawl account is self-defeating. STAGGER or serialize the Firecrawl-dependent agents.
2. **NY DOS business search is a POST form** — not queryable by any agent. This is WHY new-firm yield is always thin. Recency has never actually been filtered on; dates come from Yelp self-reported fields. Needs a scripted approach or drop the claim.
3. **Firm domains are egress-blocked for WebFetch.** Grid Hunter could not read a single payroll page. Needs `firecrawl_scrape` (not just search) to pull verbatim site language.
4. **ChamberMaster / GrowthZone directories are queryable by keyword+date** and reliably surface new tax/bookkeeping members nationally. Institutionalize this — it independently re-found 2 firms already in the pipeline, proving the channel targets the right profile.

## ~~GRID HUNTER VERIFY-LIST~~ — ⚠️ PREMISE RETRACTED 2026-08-24
**`/payrollservice.php` is NOT an in-house-payroll tell.** It is the stock URL of the **CPA Site Solutions** website template, used by hundreds of firms. It proves only that they bought the same website package. Do not use this pattern as a Grid signal again.
Original (bad) list kept for reference only:
- Zell & Ettinger CPAs, Brooklyn — ze.cpa/payrollservice.php
- A. Kahan CPA PC, Brooklyn — kahancpa.com/payrollservice.php
- TaxSmart NY, Queens — taxsmartny.com/payrollservice.php ("dedicated payroll specialist")
- Sheldon L. Richards CPA (5 boroughs) — rcpasolutions.com/payroll-services
- YWL & Company LLC, Queens — ywlcpa.com

## OUT OF SCOPE BUT NOTED
ProAxis Tax & Accounting (Dor Israel, CPA) — founded 2026, Hasbrouck Heights NJ, licensed in BOTH NJ and NY. If territory rules ever permit, this is a documented brand-new solo practice.

---

# Trigger Watcher — 2026-08-24

**Nothing material broke in the last 2 weeks.** QBO forced-automation story unchanged since July 1: no reversal, no sourceable opt-out fee, no filed lawsuit. Backlash is real but lives in unverified Intuit Community threads.

## ⚠️ TIME-SENSITIVE — WATCH DAILY
**NY DFS 2027 small group rates are still REQUESTED, not approved** (~25.3% carrier filings / 25.7% DFS summary). Last year DFS ruled **Aug 29**. A decision is likely within days.
- For 2026, DFS **cut small group requests by 45.8%**. Expect a large cut again.
- **Our TotalSource collateral must NOT quote an approved number until DFS rules.** Re-check before any printing.
- https://myportal.dfs.ny.gov/web/prior-approval/ind-and-sg-medical/summary-of-2027-requested-rate-actions

## Corrections to talking points
- **DROP the "$50/mo opt-out fee"** — unverifiable. Use cash-flow timing + loss of control instead.
- Expect the CPA counter-argument: Intuit advertises tax penalty protection when the platform errs on user-supplied data. https://quickbooks.intuit.com/payroll/tax-penalty-protection/

## NY Jan 1 2027 (known, nothing new) — CPA touchpoint material
Minimum wage moves to CPI-indexed increases; RAISE Act effective Jan 1 2027; retail panic-button rule (500+ employees, mostly outside SMB lane); 2027 PFL rate still unpublished.

## UNSWEPT (not confirmed quiet — no calls spent)
QB Desktop Payroll sunset fallout, QBOA→Intuit Accountant Suite cutover, ProAdvisor→ProPartner, Gusto/Paychex/Rippling/ADP pricing & layoffs.

## Directory Miner 2026-08-24 — 4 ProAdvisor profiles ELI MUST OPEN HIMSELF
Confirmed real Brooklyn ProAdvisor listings; profile pages egress-blocked so no contact data. Open on a non-VPN browser, ~1 min each:
- Andrew Lewis — https://proadvisor.intuit.com/quickbooks-help/andrew-lewis-cb
- Becky Rogoff (slug "accountingsolutionsny") — https://proadvisor.intuit.com/app/accountant/search?searchId=accountingsolutionsny
- Caroline Barad — https://proadvisor.intuit.com/app/accountant/search?searchId=caroline-barad-2
- Joy Lynch — https://proadvisor.intuit.com/app/accountant/search?searchId=joy-a-lynch

Rejected: Powered Books (Rockland County, SEO landing page only), TechBrot (statewide remote, no NYC office).
NOTE: Firecrawl was DISCONNECTED during this run — that's why yield was 3 not 5-8. Brooklyn ProAdvisor density is high; one unblocked pass on zips 11219/11249/11235 should triple this.

---

# Grid Hunter 2026-08-24 — retry result

## ⚠️ TOOLING CEILING (fix before running this lane again)
- **Firecrawl exposes only `firecrawl_search`** — SERP titles/snippets. **No scrape/extract tool.** No agent can read page body text.
- Firm domains remain **EGRESS_BLOCKED** for WebFetch (confirmed on ze.cpa).
- Firecrawl then 429'd and stayed there through a retry.
=> **No verbatim payroll-page language is obtainable today.** Grid Hunter cannot do its job until Firecrawl scrape is enabled OR the firm domains are allowlisted. Target URLs are already identified — it's a ~15 min job once unblocked.

## Corrections
- `/payrollservice.php` = CPA Site Solutions template. NOT a signal. (See retraction above.)
- **YWL & Company is BROOKLYN-based**, not Queens. Its Queens pages are templated geo-SEO landing pages. Watch for this pattern inflating apparent footprint.
- **Sheldon L. Richards CPA — DOWNGRADE.** Page titled "Payroll & HR Services"; the "& HR" pairing + Midtown address is the shape of a firm RESELLING a PEO/vendor bundle, not running checks in-house.

## Best remaining candidates (all UNVERIFIED — call-order, not qualification)
1. **McLan Accounting Services** — 4121 18th Ave, Borough Park — (718) 871-8250 — score 72. Only one whose payroll page is SEO-titled for the service itself ("Payroll Services Brooklyn NY"), i.e. markets payroll as a lead product. Two domains: mclantax.com / mclancpa.com.
2. **OGC-REWCPAs LLC** — 739 Utica Ave, East Flatbush — (718) 467-8535 — score 64. Multi-partner (hyphenated name implies merger); merged practices inherit two payroll processes.
3. **R Katz CPA PC** — Brooklyn 11223 — (718) 372-4800 — **Rachel Katz** — score 58. Solo principal, payroll in service list = the Slava shape.
4. **Harvey M Kraus** — 1018 8th Ave, Park Slope — (718) 788-1972 — score 55. Long-established solo; succession/Grid angle.
5. **Zell & Ettinger CPAs** — 3001 Avenue M, Midwood — (718) 692-1212 — strongest of the original five: has a SEPARATE "Online Payroll" client-entry portal ("Submit your hours and earnings whenever you want") and names NO third-party vendor. Could still be a white-labeled vendor portal.
6. **A. Kahan CPA PC** — 36 Taaffe Pl, Bed-Stuy — (718) 887-9112 — info@kahancpa.com

Book size UNKNOWN for all. Principals sourced only for Richards and Katz — rest deliberately blank, not guessed.
