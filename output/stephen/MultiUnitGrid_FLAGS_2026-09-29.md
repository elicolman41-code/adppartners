# Multi Unit Grid — Innovate Advisors — what to know before it goes to the desk
*Filled 9/29/2026 from the 9/25 CBA, the client CSV, the Paychex quarterly reports, and a web search for owner phones. Two Opus agents (data cross-check, phone hunt), one Opus QC agent, Fable ruling on every discrepancy. Every cell written is in `MultiUnitGrid_change_log_2026-09-29.txt`.*

## Open in Excel first
The file is set to recalculate on open. The derived tabs (CBA Portal, Exhibit A, both Internal COE grids) are formula-driven and populate the moment Excel opens it. Save once after opening.

## Two flags Exhibit A will print in the DM Note column
| Client | Flag | Why | One-cell fix if you want it |
|---|---|---|---|
| FRG Advisory | **Discount >60%** | $600/yr vs $1,511.40 Enhanced book = 60.3% | Product Selections: clear L27, put Yes in K27 (Essential). Book drops to $996, discount to 39.8%. |
| Wisdom by Woods | **Revenue Reduction Required** | Paychex bills $1,557.36; ADP Enhanced book for 1 EE monthly is $1,511.40. Billing exceeds book. | None needed. The excess ($45.96) is excluded from the CBA payment automatically. |

## Blank on purpose (you said leave them)
Multi Unit Grid D3 firm legal address · D9 Salesforce Acquisition ID · G6 ESO Region · G7 AC Firm ID · Product Selections N2 Conversion Agreement date · L10 branch code.

## Estimated, not confirmed
- **Next Check Date** (COE column H) by frequency: weekly 10/2, biweekly 10/9, semi-monthly 10/15, monthly 10/30, annual 12/31. Replace with real pay dates when Stephen sends them.
- **Owner phone**: verified for Upstate (561) 676-0037 [FMCSA], Kranz (484) 731-2656 [own site], Backfin (410) 498-1527 [FMCSA], Walters (718) 366-0777 [401k trustee line]. The other 9 carry Stephen's 845-642-8927.
- **Owner email**: Kranz info@kranzmotorcars.com is real. The other 12 carry sscialo@innovateadvisors.com.
- **RJC Holdings suite #491** (COE N21) came from the Florida Sunbiz filing, not from Stephen. Confirm or delete.

## Decisions applied
- **DM Deal Split set to 100%** (COE column AB; template default was 70%). House Deal Split therefore 0%. Confirm with Patrick or Shannon that October pays 100% — the vault note from 9/17 says nobody at ADP had confirmed it yet.
- Walters 3 EE (was keyed as 5). Backfin 3 EE and Auction 2 EE kept as submitted, though Paychex reports show 5 and 1.
- Walters billing $6,810.70 = ADP max, deliberately not the $13,055.90 Paychex figure.
- Wisdom corrected $1,543 → $1,557.36.
- Legal names lost their commas everywhere (form rule: letters, numbers, & and - only): "FRG Advisory LLC", "Broadway 2000 Inc".
- Provider values now match ADP's Current Provider list: "Paychex/Surepayroll", "Gusto", "Other" (Broadway, EFTPS). Notes column says plainly which two are Gusto and which one has no provider.
- Zips stored as text; NJ 08540 leading zero restored. Three cities that had state+zip jammed in were split.
- No workers comp anywhere.
- Tyree owner first name left as "Ty" (Stephen's data); payroll journal shows legal name Thomas F Tyree.

## Book vs submitted, per client (Zone 7, FY27 table in the workbook)
| Client | EE | Freq | Bundle | ADP book/yr | Submitted | Discount |
|---|---|---|---|---|---|---|
| Upstate Logistics | 3 | 26 | Enhanced | 2,603.90 | 2,042.82 | 21.5% |
| Tyree Advisory | 1 | 12 | Enhanced | 1,511.40 | 863.04 | 42.9% |
| RJC Holdings | 1 | 12 | Enhanced | 1,511.40 | 696.00 | 53.9% |
| Kranz Motorcars | 1 | 52 | Enhanced | 3,354.00 | 3,094.00 | 7.8% |
| Wisdom by Woods | 1 | 12 | Enhanced | 1,511.40 | 1,557.36 | −3.0% ⚠ |
| Auction Time Pieces | 2 | 24 | Complete | 4,366.80 | 3,698.40 | 15.3% |
| Onchain Strategies | 1 | 12 | Enhanced | 1,511.40 | 1,212.00 | 19.8% |
| Backfin Logistics | 3 | 24 | Enhanced | 2,557.20 | 2,364.00 | 7.6% |
| Walters Mirrors | 3 | 26 | HR Pro | 6,940.70 | 6,810.70 | 1.9% |
| Spencer Thwaytes | 3 | 12 | Enhanced | 1,599.00 | 924.00 | 42.2% |
| Complete Merchant | 2 | 12 | Enhanced | 1,555.20 | 1,200.00 | 22.8% |
| FRG Advisory | 1 | 12 | Enhanced | 1,511.40 | 600.00 | 60.3% ⚠ |
| Broadway 2000 | 1 | 1 | Essential | 500.00 | 400.00 | 20.0% |
| **Total** | | | | **31,033.80** | **25,462.32** | **18.0%** |

2x proxy on submitted billing: **$50,924.64**. Not a payout number — the desk prices each account.

## Still not in the workbook because nobody has it
Firm legal address · owner emails for 12 clients · real pay dates · any signature.
