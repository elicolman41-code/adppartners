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

/** Generate params for team/decade categories, retrying until playable. */
function generateParams(def: CategoryDefinition, rng: Rng): CategoryParams | null {
  if (!def.needsParams || def.needsParams.length === 0) return def.params ?? {};

  for (let attempt = 0; attempt < 40; attempt++) {
    const params: CategoryParams = { ...def.params };
    if (def.needsParams.includes('team')) params.teamId = pickOne(rng, TEAMS).id;
    if (def.needsParams.includes('decade')) params.decade = pickOne(rng, DECADES);
    if (eligibleCount(PLAYERS, def.validatorKey, params) >= MIN_ELIGIBLE) return params;
  }
  return null;
}

/**
 * Spin the next category. Excludes definitions already used this match,
 * checks eligible-player counts, and balances difficulty by round:
 * early rounds lean easy, later rounds lean hard.
 */
export function spinCategory(rng: Rng, usedDefinitionIds: string[], roundIndex: number, totalRounds: number): SpunCategory {
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
    const params = generateParams(def, rng);
    if (params === null) continue;
    if (eligibleCount(PLAYERS, def.validatorKey, params) < MIN_ELIGIBLE) continue;
    return {
      definitionId: def.id,
      label: resolveLabel(def, params),
      validatorKey: def.validatorKey,
      params,
    };
  }

  // Every category exhausted (cannot happen with 30 defs / 5 rounds), but
  // fail safe to the broadest category.
  const fallback = CATEGORIES.find((c) => c.id === 'cat-all-star')!;
  return {
    definitionId: fallback.id,
    label: fallback.label,
    validatorKey: fallback.validatorKey,
    params: {},
  };
}
