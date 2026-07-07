import type { CategoryDefinition, CategoryParams, SpunCategory } from '../types';
import { CATEGORIES } from '../data/categories';
import { PLAYERS } from '../data/db';
import { TEAMS, teamName } from '../data/teams';
import { eligibleCount } from './validators';
import { pickOne, type Rng } from './rng';

// A category is only playable if enough seeded players satisfy it —
// otherwise typing a correct answer becomes near-impossible.
export const MIN_ELIGIBLE = 6;

const DECADES = [1980, 1990, 2000, 2010, 2020];

function resolveLabel(def: CategoryDefinition, params: CategoryParams): string {
  return def.label
    .replace('{team}', params.teamId ? teamName(params.teamId) : '?')
    .replace('{decade}', params.decade !== undefined ? String(params.decade) : '?');
}

/** Generate playable params for a category (checks MIN_ELIGIBLE against the pool). */
function generateParams(def: CategoryDefinition, rng: Rng, pool: typeof PLAYERS): CategoryParams | null {
  if (!def.needsParams || def.needsParams.length === 0) {
    const params = def.params ?? {};
    return eligibleCount(pool, def.validatorKey, params) >= MIN_ELIGIBLE ? params : null;
  }

  for (let attempt = 0; attempt < 40; attempt++) {
    const params: CategoryParams = { ...def.params };
    if (def.needsParams.includes('team')) params.teamId = pickOne(rng, TEAMS).id;
    if (def.needsParams.includes('decade')) params.decade = pickOne(rng, DECADES);
    if (eligibleCount(pool, def.validatorKey, params) >= MIN_ELIGIBLE) return params;
  }
  return null;
}

/** Every param combination a category can spin with. */
function allParamCombos(def: CategoryDefinition): CategoryParams[] {
  if (!def.needsParams || def.needsParams.length === 0) return [def.params ?? {}];
  const teams = def.needsParams.includes('team') ? TEAMS.map((t) => t.id) : [undefined];
  const decades = def.needsParams.includes('decade') ? DECADES : [undefined];
  const combos: CategoryParams[] = [];
  for (const teamId of teams) {
    for (const decade of decades) {
      const params: CategoryParams = { ...def.params };
      if (teamId !== undefined) params.teamId = teamId;
      if (decade !== undefined) params.decade = decade;
      combos.push(params);
    }
  }
  return combos;
}

/**
 * How many category definitions are still playable (≥ MIN_ELIGIBLE eligible
 * players, in at least one param combination) once `excludeIds` are out of
 * the pool. Run-it-back uses this to know when the pool is drafted out.
 */
export function playableCategoryCount(excludeIds: ReadonlySet<string>): number {
  const available = excludeIds.size === 0 ? PLAYERS : PLAYERS.filter((p) => !excludeIds.has(p.id));
  let count = 0;
  for (const def of CATEGORIES) {
    if (allParamCombos(def).some((params) => eligibleCount(available, def.validatorKey, params) >= MIN_ELIGIBLE)) {
      count++;
    }
  }
  return count;
}

/**
 * Spin the next category. Excludes definitions already used this match,
 * checks eligible-player counts against the *available* pool (players
 * drafted this game or in earlier games of a run don't count), and balances
 * difficulty by round: early rounds lean easy, later rounds lean hard.
 */
export function spinCategory(
  rng: Rng,
  usedDefinitionIds: string[],
  roundIndex: number,
  totalRounds: number,
  excludeIds: ReadonlySet<string> = new Set(),
): SpunCategory {
  const available = excludeIds.size === 0 ? PLAYERS : PLAYERS.filter((p) => !excludeIds.has(p.id));
  const progress = totalRounds <= 1 ? 0 : roundIndex / (totalRounds - 1);
  const targetDifficulty: 1 | 2 | 3 = progress < 0.34 ? 1 : progress < 0.67 ? 2 : 3;

  const unused = CATEGORIES.filter((c) => !usedDefinitionIds.includes(c.id));
  const pool = unused.length > 0 ? unused : CATEGORIES;

  // Prefer the target difficulty, fall back to neighbors, then anything.
  let candidates = pool.filter((c) => c.difficulty === targetDifficulty);
  if (candidates.length === 0) {
    candidates = pool.filter((c) => Math.abs(c.difficulty - targetDifficulty) === 1);
  }
  if (candidates.length === 0) candidates = pool;

  // Try candidates in random order until one is playable.
  const shuffled = [...candidates].sort(() => rng() - 0.5);
  for (const def of [...shuffled, ...pool]) {
    const params = generateParams(def, rng, available);
    if (params === null) continue;
    return {
      definitionId: def.id,
      label: resolveLabel(def, params),
      validatorKey: def.validatorKey,
      params,
    };
  }

  // Every category is below MIN_ELIGIBLE against the shrunken pool (very deep
  // run-it-back chain). Fail safe to whichever category still has the most
  // available eligible players so the round stays winnable as long as possible.
  let best: { def: CategoryDefinition; params: CategoryParams; n: number } | null = null;
  for (const def of CATEGORIES) {
    for (const params of allParamCombos(def)) {
      const n = eligibleCount(available, def.validatorKey, params);
      if (!best || n > best.n) best = { def, params, n };
    }
  }
  const fb = best!;
  return {
    definitionId: fb.def.id,
    label: resolveLabel(fb.def, fb.params),
    validatorKey: fb.def.validatorKey,
    params: fb.params,
  };
}
