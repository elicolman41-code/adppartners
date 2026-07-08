import type { Match, Player } from '../types';
import { PLAYERS } from '../data/db';
import { makeRng, type Rng } from './rng';
import { validatePick } from './validators';
import { hasLanded, unavailableIds } from './match';
import { buildLineup } from './lineup';

export type AiLevel = 'rookie' | 'veteran' | 'goat';

export const AI_LEVELS: { level: AiLevel; name: string; blurb: string }[] = [
  { level: 'rookie', name: 'Rookie Bot', blurb: 'Knows some ball. Misses picks, drafts on vibes.' },
  { level: 'veteran', name: 'Coach Bot', blurb: 'Solid picks, the occasional brain-fade.' },
  { level: 'goat', name: 'GOAT Bot', blurb: 'Never misses. Drafts for talent AND lineup fit.' },
];

export function aiName(level: AiLevel): string {
  return AI_LEVELS.find((l) => l.level === level)!.name;
}

/** Chance the AI blows a pick on purpose (types a wrong-category player). */
const MISS_CHANCE: Record<AiLevel, number> = { rookie: 0.35, veteran: 0.12, goat: 0 };

/** Raw draft value: star tier first, then bucket ratings. */
function talentScore(pl: Player): number {
  const r = pl.ratings;
  const avg = (r.scoring + r.creation + r.shooting + r.perimeterDefense + r.rimProtection + r.rebounding) / 6;
  return (6 - pl.tier) * 25 + avg;
}

/** Bonus for filling a lineup slot the AI doesn't have covered yet. */
function fitBonus(pl: Player, roster: string[]): number {
  const { slots } = buildLineup(roster);
  return pl.positions.some((pos) => slots[pos] === null) ? 18 : 0;
}

/**
 * The AI's pick for the current turn. Deterministic per match + round +
 * attempt (seeded), so reloading replays the same draft. Returns a display
 * name ready for submitPick. Difficulty tunes miss rate and pick quality.
 */
export function aiPickName(match: Match, level: AiLevel): string {
  const round = match.rounds[match.currentRound];
  const rng = makeRng(`ai:${match.id}:r${match.currentRound}:a${round.attempts.length}`);

  const gone = unavailableIds(match);
  for (const a of round.attempts) gone.add(a.pick.playerId);
  const available = PLAYERS.filter((pl) => !gone.has(pl.id));

  const eligible: Player[] = [];
  const ineligible: Player[] = [];
  for (const pl of available) {
    (validatePick(pl, round.category).eligible ? eligible : ineligible).push(pl);
  }

  // A deliberate miss: reach for a big name that doesn't actually qualify.
  if (eligible.length === 0 || rng() < MISS_CHANCE[level]) {
    const pool = ineligible.length > 0 ? ineligible : eligible;
    const stars = [...pool].sort((x, y) => talentScore(y) - talentScore(x)).slice(0, 15);
    return pick(rng, stars).displayName;
  }

  const roster = match.participants[match.turn].roster;
  const ranked = [...eligible].sort(
    (x, y) => talentScore(y) + fitBonus(y, roster) - (talentScore(x) + fitBonus(x, roster)),
  );

  if (level === 'rookie') return pick(rng, ranked).displayName; // any eligible player
  if (level === 'veteran') return pick(rng, ranked.slice(0, 8)).displayName; // good pick
  return ranked[0].displayName; // GOAT: best available for talent + fit
}

function pick<T>(rng: Rng, arr: T[]): T {
  return arr[Math.floor(rng() * arr.length)];
}

/** Whether the side whose turn it is is an AI (and should auto-pick). */
export function aiOnClock(match: Match): AiLevel | null {
  if (match.phase !== 'pick') return null;
  const side = match.participants[match.turn];
  if (!side.ai) return null;
  // Safety: never auto-pick for a side that already landed this round.
  if (hasLanded(match, match.currentRound, match.turn)) return null;
  return side.ai;
}
