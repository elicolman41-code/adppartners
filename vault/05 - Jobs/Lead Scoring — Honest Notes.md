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

---

# Gated sweep 2026-08-31 (Eli asked for a strict approval loop)

## THE BAR (4 hard requirements — apply every round)
1. WORKING PHONE with a source URL. A firm without a phone is NOT a lead — exclude it.
2. REAL WEBSITE — established operation, not a bare state filing.
3. **PAYROLL IN THEIR OWN SERVICE LIST.** A Yelp/YellowPages CATEGORY TAG DOES NOT COUNT. (Emerson Gamory was rejected on exactly this and later confirmed to have NO payroll — the tag was wrong. The rule earned its keep.)
4. NOT BRAND-NEW — roughly 3-15 yrs. Established with a book and a site.

## APPROVED (8) → on the board
Arrowpoint Tax (92) · Donofrio (84) · AJ Tax (82) · J.D. Pantzis (80) · Alan Lorman (78) · Manning Accounting (74) · Shibu P. Thomas (74) · Brooklyn CPA P.C. (62)

## REJECTED, with reasons — do not re-surface
- **Shay CPA** — ALREADY A LIVE PIPELINE ACCOUNT (Nina & Akshay). My prompt error: exclusion lists must include PIPE accounts, not just LEADS.
- **Pay Plus Accounting Solutions / Anays Caceres** — Eli has ALREADY met with Anays. Same error class.
- **Emerson Gamory** — payroll DISPROVEN. Own site + TaxBuzz + BBB + chamberofcommerce + Black Atlas all list tax prep/planning/bookkeeping/estate/formation, NO payroll. Only the Yelp category said otherwise.
- **Brooklyn Bookkeeping Co** — their own copy says payroll "in partnership with ADP." ALREADY AN ADP PARTNER. → Eli should Salesforce-check who owns them.
- **Gabor & Associates** — no payroll in services.
- **Staten Island Tax Services** — no named principal, no confirmed website.
- **Dynamic Tax & Accounting** — multi-branch chain (Bronx/Queens/Buffalo/NJ), branch office not a principal's shop.
- **New Era Tax Service** — 3 yrs, BBB accredited Jan 2026, rebrand of Smart Tax. Fails establishment.
- **All In Accounting (SI)** — payroll directory-only, same defect as Gamory.
- **Marcus Hilton CPA / Rodriguez & Co (Bronx)** — no payroll text obtained. Re-workable.
- **DTGD CPAs / DeCandido (SI)** — /payrollservice.php template, non-signal.

## ⚠️ PROMPT FIX REQUIRED EVERY SWEEP
Exclusion lists MUST include the LIVE PIPELINE accounts, not just the leads array. Two agents surfaced existing relationships as cold leads this round (Shay, Pay Plus). Pull names from BOTH arrays.

## EGRESS — now blocked to WebFetch (cumulative)
gusto.com · accountants.ramp.com · directory.relayfi.com · xero.com · yelp.com · yellowpages.com · taxbuzz.com · dayonelead.com · most firm domains.
Phone-bearing detail records are the method's foundation and they are increasingly unreadable. Firecrawl is SEARCH-ONLY (no scrape). **The binding constraint is now fetch access, not search strategy.**
Untried and worth it: **PTIN Directory by ZIP** — never reached before a cap.

## COVERAGE STILL EMPTY
Bronx: Riverdale, Kingsbridge, Throgs Neck, Pelham Bay, Soundview, Mott Haven, Hunts Point, Castle Hill, Parkchester.
Staten Island: St. George, Port Richmond, New Brighton, West Brighton, Bulls Head, Great Kills.
Both boroughs collapse into CPA Site Solutions template sites and unfetchable category pages.

---

# 🎯 THE HIGHEST-VALUE PROFILE (Eli, 2026-08-31) — "big book, small footprint"

## What it is
The UNDER-PROSPECTED firm: a long-tenured neighborhood tax/accounting practice with a LARGE client book but almost no marketing presence. No SEO, no content, no partner-directory listing. **No rep has ever called them.** When they engage a vendor they call an inbound 800 number and get a junior inside salesperson who doesn't recognize what they're holding.

**Proof case Eli cited:** the principal of Orient Star Services (orientstarservices.com, Sadique) called ADP's inbound line saying "I have a hundred clients." A colleague picked it up and turned it into a **200-client Grid acquisition.**

## Why it's an arbitrage
These firms are invisible to search — no domain authority, no SEO — which is EXACTLY why no competitor and no ADP rep has found them. The invisibility that makes them hard for us to find is the same thing that makes them uncontested.
(Confirmed: orientstarservices.com is egress-blocked AND a name search returns nothing about the firm. The exemplar itself is unfindable.)

## SIGNALS (target FIRM CHARACTERISTICS — never ethnicity or national origin)
- Storefront/small-office practice in a dense immigrant small-business corridor
- **Multilingual service advertised** — a commercial signal that the client base is small-business owners needing hands-on service
- **10+ years tenure + basic/dated website** — real operation, no marketing machine
- **Multi-service**: entity formation, notary, translation, immigration paperwork, insurance alongside tax/bookkeeping
- **ABSENT from Gusto / ProAdvisor / Xero partner directories** — presence there means someone already found them
- High review count relative to web sophistication = real client volume

## TERRITORY
South Brooklyn: Sheepshead Bay 11235 · Homecrest 11229 · Brighton Beach · Gravesend 11223 · Bensonhurst 11214/11204 · Midwood 11230 · Bay Ridge 11209 · Dyker Heights 11228
Queens: Flushing 11354/11355 · Elmhurst 11373 · Jackson Heights 11372 · Corona 11368 · Woodside 11377 · Richmond Hill 11418 · Ozone Park · Jamaica 11432 · Astoria · Ridgewood 11385

## THE RIGHT TOOL — PTIN Directory (ptindirectory.com)
Lists EVERY IRS-registered paid preparer by city/ZIP **including firms with zero web presence** — precisely this population. Carries firm name AND preparer name, so it yields a named principal for an otherwise invisible firm. Never used before this run. This is the correct instrument for this profile; directory-partner mining is structurally the WRONG one (it selects for firms already found).

## SCORING FOR THIS PROFILE
Actionability 25 / Business-client evidence 20 / Book-size signals 20 (tenure, review volume, staff, service breadth) / **Under-prospected signals 20** (no partner-directory listing, basic website, no marketing) / Proximity 15.
Note the inversion: for this lane, ABSENCE from partner directories SCORES POSITIVELY. That is the opposite of the referral lane's rule.

## PTIN METHOD — RESULTS 2026-08-31 (7 leads, the profile works)
**ptindirectory.com is EGRESS-BLOCKED to WebFetch — but its Google SNIPPETS render firm name, preparer name, full street address AND phone.** That is enough. Never fetch it; always snippet-mine it.
**How to query:** ZIP numbers do NOT filter (URLs carry no ZIP). What works is "ptindirectory Brooklyn" + a firm-name token ("accounting corp", "accounting services corp") OR a street/neighborhood name. For unswept areas query by CORRIDOR: "ptindirectory Brooklyn 86th Street" / "Kings Highway" / "Coney Island Avenue" / "Bay Ridge Avenue".
Also use **ptin.org** — a SEPARATE site with FIRM-level records (more useful than preparer-level). It produced Juan V. Soto's credentials and Brighton Tax's firm record.

**ZIP yield:** 11229 Homecrest = RICHEST (9 named firms w/ phones in one query) · 11235 Brighton Beach = good · 11214/11223 = poor (engine ignores ZIP, matches "Brooklyn") · 11204/11230/11234/11209/11228 = NOT REACHED.
**Budget rule:** snippet-mining is cheap, VERIFICATION burns the calls (~every 2nd detail page is blocked). Spend ~2/3 of the cap on verification, not discovery.

## NEWLY EGRESS-BLOCKED (cumulative dead-ends)
ptindirectory.com · dotax.com · buzzfile.com · chamberofcommerce.com · yelp.com · yellowpages.com · taxbuzz.com · gusto.com · accountants.ramp.com · directory.relayfi.com · xero.com · dayonelead.com · AND ordinary small-business sites (taxofficenyc.com, ccltax.com, sotosaccountingservices.com, orientstarservices.com).
Still yielding via snippets: Manta · Yahoo Local · ZoomInfo · CountingWorks · ptin.org · bizprofile.net · i24app.com

## ⚠️ VERIFY BEFORE DIALING
- **Blue-Ribbon Accounting & Tax (Elmhurst, Eric Chung)** — possible name collision with Eli's "Jacob at Blue Ribbon" TotalSource account. Likely different firms; CONFIRM before cold-calling.
- **United Accounting Services (Ilya Estrin, 2946 Quentin Rd)** — 17 yrs, payroll in services, would otherwise qualify. EXCLUDED: BBB Scam Tracker entry reports a recruiting email IMPERSONATING the firm, and phone numbers conflict across sources. The report is about impersonation, not misconduct by them — but get a clean phone before dialing.

## ONE VERIFICATION QUERY SHORT (cheap to close next run)
Shneyder CPA PC (Roman Shneyder, 174 Brighton 11th St 2nd Fl 11235, 347-875-0070) · Esses Accounting Firm LLC (Victor Esses, 2171 E 21st St 11229, 718-615-1684) · Leon Levitis Accounting (address conflict: 1817 vs 807 Kings Hwy) · Fajardo Accounting (43-20 52nd St, Woodside — payroll advertised, no phone yet)

## UNSWEPT
Brooklyn: 11204, 11230, 11234, 11209, 11228. Queens: Astoria, Ridgewood 11385, Sunnyside, Rego Park, Forest Hills, Ozone Park, Corona 11368 — **Corona and Ridgewood highest-yield remaining.**
