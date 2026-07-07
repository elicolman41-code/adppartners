# Draft Spin 🏀

Head-to-head NBA category draft game, built from the *Draft Spin* product
brief (July 2026). Spin a random category, type any NBA player, get
fact-checked instantly by a deterministic rules engine, and after 5 rounds
watch both drafted teams battle in a simulated best-of-7 series.

## Play it

Open **`dist/index.html`** in any browser — it is a fully self-contained
single file (works on a phone, no server, no install). Pass-and-play: two
players share one device.

## Rules (from the brief)

- **Eligible pick:** +1 point, player locks into your roster.
- **Ineligible real player:** −1 point, with the exact reason and evidence.
- **Duplicate player (anywhere in the match):** −1 point.
- **Unknown name / typo:** 0 points, retry — you are only penalized after
  submitting a real player.
- **Series win:** +3 bonus points.

Non-negotiables honored: eligibility is checked by **code against structured
data** (never AI guessing), no live API calls during a round, no copied brand
assets, and the series simulation is **seeded by match id** so reloading the
room replays the identical result.

## What's inside

| Piece | Where |
|---|---|
| 160+ curated players (bio, height, draft, country, awards, rings, team-season stints, source notes) | `src/game/data/players*.ts` |
| 30 launch categories with difficulty + params | `src/game/data/categories.ts` |
| Deterministic validators returning `{eligible, reason, penalty, player, evidence[]}` | `src/game/engine/validators.ts` |
| Alias-aware search (KD, Bron, Shaq, T-Mac…), accent/punctuation normalization, top-8 suggestions | `src/game/engine/search.ts` |
| Category generator: no repeats, eligible-count checks, random team/decade params, difficulty ramp | `src/game/engine/categoryGen.ts` |
| Match state: rooms, rounds, turns, scoring, duplicate prevention, localStorage persistence | `src/game/engine/match.ts` |
| Series simulator: talent/creation/spacing/defense/rebounding + fit penalties, seeded best-of-7, game scores, closing notes, MVP, why-you-won | `src/game/engine/simulator.ts` |

## Develop

```bash
npm install
npm run dev      # local dev server
npm test         # 70 unit tests (validators, search, match flow, simulator)
npm run build    # emits the single-file dist/index.html
```

## Data notes

Seed data is hand-curated from public career records (July 2026) with a
source note on every player, per the brief's audit requirement. Historical
franchises map to current ids (SuperSonics→OKC, NJ Nets→BKN, Bullets→WAS,
NO Hornets→NOP). For a commercial release, swap the seed for a licensed
provider (SportsDataIO / Sportradar) as the brief recommends — the validator
layer doesn't change.
