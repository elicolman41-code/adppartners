# Bank Proof Requirements (ADP SBS, updated 4.2.26)
*Source: ADP email "Updated Bank Proof Requirements 4.2.26" (sbshrs.adpinfo.com), read 2026-09-28. Otto always holds the current list — check Otto before arguing a rejection.*

Applies when submitting a new order OR updating a bank account.

## Gating rules (fail these and nothing else matters)
- **U.S.-based CHECKING account only.** Savings, cash management, and lines of credit are rejected.
- Name on the account must match the **legal or DBA name on the CAA**. A nickname is not a name.
- Routing and account number must match the CAA.

## The two forms Eli will actually use
Voided checks are effectively dead — most small clients don't have a checkbook. Plan around statements and screenshots.

### Bank Statement
- Timestamped, dated within 30 days
- Company name · Bank name
- **ACH/electronic ABA** — not the wire routing number
- **Full unmasked DDA**
- **All pages**, no edits, no handwriting, no redaction
- Minimum balance $0.00 (a negative balance fails)

**Where this breaks:** most statements print the account number but no routing number at all, or print the *wire* routing number, which is a different number than the ACH routing at Chase, BofA, and others. If the statement is missing the ACH ABA or shows a masked DDA, it is not a valid proof on its own — go to a screenshot instead of arguing.
Second break: "all pages, no redaction" means the client hands over full transaction history. Some will refuse. Screenshot is the lower-friction path.

### Screenshot of Online Bank Account
- Dated within 30 days, with a **timestamp showing the date**
- **Whole screen, not cropped**
- Company name — **not a nickname**
- **Bank name/logo visible**
- ACH/electronic ABA
- **Full unmasked DDA** (most mobile apps mask by default — client must tap the reveal/eye icon first)
- Desktop or mobile both fine
- **Mobile two-shot allowance:** if the date can't fit in one screenshot, a second screenshot showing **last login date + bank name + last four of the account** is accepted

**Practical:** desktop browser is usually easier than mobile because the OS clock shows the date. On mobile the status bar shows time but not date, which is exactly why the two-shot allowance exists.

## CORRECTION 2026-09-28 — two proofs CAN be combined
Eli, from direct experience: **two different bank proofs can be submitted together to make one complete proof.** Example: a statement that shows the full account number but no routing, plus a screenshot that shows the routing.

The 4.2.26 email does NOT say this — it reads as if each form is judged on its own ("must contain the items listed in order to be considered valid"). Fable pushed back on this and was wrong. Do not push back on it again. Otto governs, and the email is a summary.

## Other accepted forms (reference only)
- **Voided check:** fractional number, company name, bank name, ABA + DDA, "VOID" written, no other handwriting
- **Pre-printed check reorder form:** company name, bank name, ABA + DDA, pre-printed "reorder" wording; no VOID needed
- **Bank confirmation / verification letter:** company name, bank name, ACH ABA, full unmasked DDA, signed by banker AND authorized signer, **plus (new 4.2.26) timestamped, dated within 30 days, banker name and phone number**
- **Bank signature card:** company name, bank name, ACH ABA, full unmasked DDA, signed by banker and authorized signer

## Pre-send checklist for a client screenshot
1. Desktop browser if possible, so the date is on screen
2. Log in, open the business checking account detail page
3. Tap/click to **unmask the full account number**
4. Confirm the **company legal/DBA name** appears, not a nickname
5. Confirm the **bank logo** is in frame
6. Capture the **entire screen** — no cropping
7. If mobile and no date on screen, take the second shot of the last-login screen
