# Lead Scoring — what's real and what isn't

## ⚠️ THE SCORES ON THE BOARD ARE ESTIMATES, NOT MEASUREMENTS
They are agent judgments on unverified data. Different agents have scored the same signal differently. **No score has ever been validated against a call outcome.** Do not present them to Eli as if they were measured. The Lane Scorecard on the dashboard is the only measured number in the system.

## THE STRUCTURAL BIAS I BUILT AND HAVE TO CORRECT
Directory-record mining (Yelp / YellowPages / Manta / TaxBuzz / PTIN / BBB) is the highest-yield method for getting phone numbers — and it systematically returns **STOREFRONTS**, because storefronts are what live in those directories.

**It is structurally blind to the profile Eli actually wants** (the DCO Partners profile): new partner-style firms with modern websites, minimal directory footprint, tax/advisory branding, payroll present but deliberately not advertised.

=> Optimizing for actionability optimized for findability, which selected for the wrong firms. Two different methods are needed:
- **Storefront/community lane** → directory-record mining (works, keep it)
- **DCO/partner-firm lane** → website COPY-PATTERN search, spin-off/launch press, DayOneLead DOS filings, LinkedIn founder searches. NEVER directory mining.

## THE DCO PROFILE (confirmed by Eli 2026-08-24)
All four required:
1. NEW — founded ~2023-2026
2. Brands as TAX / ADVISORY — not as a payroll provider. Payroll is a buried line item.
3. PARTNER-STYLE firm — 2+ principals, modern site, "Partners"/"Advisors"/"& Co." naming. NOT a walk-in storefront.
4. Serves SMALL BUSINESSES (employers), not primarily individual 1040 filers.
Reference: dcopartners.com (egress-blocked to our tools — Eli can open it).

## BOARD DIRECTION
Eli's call (2026-08-24): **keep growing the total board.** Do not prune for the sake of a short list. But bias new additions toward the DCO profile, and stop treating raw count as progress.

## FEEDBACK LOOP — now live
Dashboard has a **Lane Scorecard** that computes meeting-set rate per tag from Eli's own logged call outcomes (2+ outcomes per lane to appear). It runs in HIS browser only.
**Fable cannot see it.** Eli clicks "Copy my status" and pastes; only then can scoring be re-weighted against real results.
=> ASK FOR THE STATUS PASTE. Without it every score stays a guess.

---

# 2026-08-24 — THE DIAGNOSTIC FINDING

## Web search CANNOT see the DCO profile. This is structural.
An agent searched `"DCO Partners"` directly. **It returned nothing about DCO Partners — not even its own website.** The reference firm Eli handed us is invisible to the search backend.

Root cause: the search layer ranks by DOMAIN AUTHORITY. A 2-year-old firm's site loses every query to the same ~12 SEO aggregators (1-800Accountant, GTA Accounting, Xendoo, Clutch, Dimov, ClearPath). **If the exemplar is invisible, every firm matching its profile is invisible by construction.**

=> STOP running keyword sweeps at this profile. No query phrasing fixes a ranking problem.

## RETIRED HYPOTHESES (do not retry)
- **Trade-press launch coverage** — Accounting Today / CPA Practice Advisor cover top-500 M&A and software launches. Two people quietly opening a PLLC is orders of magnitude below their floor. This vein does not exist.
- **Founding-date phrases as search terms** ("founded in 2024", "since 2023") — never matched real site copy; new firms rarely put a founding year on the homepage. Pure query dilution.
- **`site:linkedin.com/company`** — WebSearch does NOT honor site: operators; it silently degrades to a generic query and returns Wikipedia articles about CLA and RSM.
- **Website copy-pattern queries** — right instinct, but defeated by the domain-authority ranking above.

## ✅ THE UNLOCK — DayOneLead via WebSearch allowed_domains
WebFetch is HARD-BLOCKED on dayonelead.com. **But `WebSearch` with `allowed_domains:["dayonelead.com"]` makes the summarizer READ the listing pages and enumerate business names + filing dates.** This is currently the ONLY verified-date channel we have.

Confirmed live pages: /new-york/brooklyn/accounting (19) · /brooklyn/bookkeeping (5) · /brooklyn/business-consulting (111) · /queens/tax-preparation · /manhattan/tax-preparation (19) · /manhattan/financial-services (372) · /manhattan/business-consulting (135) · /bronx/tax-services (6) · /staten-island/business-services (8). Brooklyn accounting most-recent filing: Jun 10 2026 — the data is current.

**TWO-STAGE PIPELINE (use this every sweep):**
1. WebSearch with allowed_domains dayonelead.com, phrased to make the summarizer ENUMERATE names + filing dates, one borough-industry page per call.
2. Then NAME-SEARCH each partner-style hit individually — name-first searches work where profile-first searches fail (proved: "Cipriani & Bauer" returned partners, address, phone and emails in ONE call).

## Names harvested 2026-08-24 (DOS-sourced)
Brooklyn accounting: Frio · Yavel and Associates · Weiss & Company · RD Williamson & Assoc · Cipriani & Bauer · Rosmerta Ventures Management · GLAT Bookkeeping
Manhattan tax prep: Williams Tax Services · Vital NextVentures · Ramos Tax Associates · Forte Tax · AS Tax & Accounting · Genuine Tax Solutions
REJECTED: Cipriani & Bauer (Bauer 24+ yrs, co-op/condo/HOA audit specialty — not new, not small-biz) · Yavel and Associates (solo profile) · Sigma Accountants & Advisors (incorporated 2017, single principal) · Mainline Partners (est. 1994)

## BEST DCO MATCH ON THE BOARD
**Velo Accounting Group LLC** — Brooklyn 11201, walking distance from DUMBO. Payroll listed among bookkeeping/sales tax/strategic finance (present, not headlined). **Already in the Gusto partner directory** = proven referrer, so the conversation is displacement not education. No phone, no confirmed principal — Eli can open veloag.com himself.

## THE CHANNEL WORTH MORE THAN ANY SWEEP
**Ask DCO Partners for referrals.** Firms founded in the same 2-3 year window by people who left the same mid-size firms cluster socially. One conversation with DCO's principals would out-produce a hundred searches. This is the highest-leverage move available and costs nothing.
