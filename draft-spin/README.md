# Draft Spin 🏀

Head-to-head NBA category draft game, built from the *Draft Spin* product
brief (July 2026). Spin a random category, type any NBA player, get
fact-checked instantly by a deterministic rules engine, and after 5 rounds
watch both drafted teams battle in a simulated best-of-7 series.

## Play it

Open **`dist/index.html`** in any browser — it is a fully self-contained
single file (works on a phone, no server, no install). Pass-and-play: two
players share one device.

## Rules

- **Eligible pick:** the player slots into your lineup (Point Guard, Shooting
  Guard, Small Forward, Power Forward, Center — multi-position players slide
  to wherever they're needed).
- **Ineligible real player:** ✕ — the player is crossed out and the turn
  passes to the other player *on the same category* (the exact reason +
  evidence is shown). You get the turn back until you land one — both sides
  always finish with five players.
- **Duplicate player (this game or an earlier game of the run):** ✕ — same
  as a wrong pick.
- **Unknown name / typo:** free retry, no penalty.
- **Winner:** the simulated best-of-7 between the two drafted lineups decides
  the game — every clean pick makes your team stronger.
- **Run it back:** chain game after game with the same matchup. Every player
  drafted earlier in the run is out of the pool for both sides, and the run
  scoreboard tracks games won.

Non-negotiables honored: eligibility is checked by **code against structured
data** (never AI guessing), no live API calls during a round, no copied brand
assets, and the series simulation is **seeded by match id** so reloading the
room replays the identical result.

## What's inside

| Piece | Where |
|---|---|
| 230+ curated players through the 2025-26 season (bio, height, draft, country, awards, rings, team-season stints, multi-position tags, source notes) | `src/game/data/players*.ts` |
| Lineup builder: assigns picks to PG/SG/SF/PF/C slots, multi-position players fill gaps | `src/game/engine/lineup.ts` |
| 30 launch categories with difficulty + params | `src/game/data/categories.ts` |
| Deterministic validators returning `{eligible, reason, player, evidence[]}` | `src/game/engine/validators.ts` |
| Alias-aware search (KD, Bron, Shaq, T-Mac…), accent/punctuation normalization, top-8 suggestions | `src/game/engine/search.ts` |
| Category generator: no repeats, eligible-count checks, random team/decade params, difficulty ramp | `src/game/engine/categoryGen.ts` |
| Match state: rooms, rounds, steal-rule turn passing, X-out rulings, run-it-back chaining, duplicate prevention, localStorage persistence | `src/game/engine/match.ts` |
| Series simulator: talent/creation/spacing/defense/rebounding + fit penalties, seeded best-of-7, game scores, closing notes, MVP, why-you-won | `src/game/engine/simulator.ts` |

## Develop

```bash
npm install
npm run dev      # local dev server
npm test         # 91 unit tests (validators, search, match flow, steal rule, run-it-back, lineup, simulator, data integrity)
npm run build    # emits the single-file dist/index.html
```

## Data notes

Seed data is hand-curated from public career records (July 2026) with a
source note on every player, per the brief's audit requirement. Historical
franchises map to current ids (SuperSonics→OKC, NJ Nets→BKN, Bullets→WAS,
NO Hornets→NOP). For a commercial release, swap the seed for a licensed
provider (SportsDataIO / Sportradar) as the brief recommends — the validator
layer doesn't change.
