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

## GRID HUNTER VERIFY-LIST (unverified — need scrape pass, do NOT cold call on this alone)
Self-hosted `/payrollservice.php` pattern = usually in-house payroll:
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
