# Job: Manual 401(k) remittance to Paychex during conversion
Use when payroll moves to ADP but the Paychex (HRS) 401(k) hasn't converted yet. First used: Upstate (10/2026).

## ADP side (Eli / implementation)
1. In RUN set up 401(k) deductions (pre-tax / Roth %) per enrolled EE.
2. Mark as employee deductions NOT remitted by ADP (withhold only).
3. Skip non-participants.
4. After each payroll, pull amounts from RUN Payroll Register / Deductions report.

## Paychex side (client, every payroll)
- One-time call: Paychex Retirement Services 1-800-472-0072 — "Payroll moved to ADP; how do we submit 401(k) contributions manually until conversion?" (confirm upload vs entry + funding)
- Typical (VERIFY on call): Paychex Flex → Retirement → Contributions → Submit/Enter (Remit) Contributions → enter pay date + EE deferrals + ER match → submit; Paychex drafts company bank.
- Timing: right after each payday (DOL: as soon as practicable; practically within a few days).
- Ends when ADP 401(k) conversion (McKenzie) is live.

## Upstate amounts (from 10/02 Paychex check; use ADP actuals)
Brogan pre-tax 6% ~$403.85 + ER match ~$269.23 · Reid Roth 8% ~$461.54 + ER match ~$230.77 · Robson not enrolled · Total ~$1,365.39/payroll
