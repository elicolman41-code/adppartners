import type { Player, SeriesResult, SimGame, TeamRatingBreakdown } from '../types';
import { PLAYER_BY_ID } from '../data/db';
import { makeRng, pickOne, randomInt, type Rng } from './rng';

// Turns two drafted rosters into a seeded best-of-7. The goal is a fun,
// defensible result that rewards talent AND fit — not a real projection.

const TIER_TALENT: Record<number, number> = { 1: 96, 2: 86, 3: 74, 4: 62, 5: 50 };

function avg(nums: number[]): number {
  return nums.length === 0 ? 0 : nums.reduce((s, n) => s + n, 0) / nums.length;
}

export function rateRoster(playerIds: string[]): TeamRatingBreakdown {
  const players = playerIds.map((id) => PLAYER_BY_ID[id]).filter(Boolean) as Player[];
  if (players.length === 0) {
    return {
      talent: 0, creation: 0, spacing: 0, perimeterDefense: 0, rimProtection: 0,
      rebounding: 0, fitPenalty: 0, fitNotes: ['No eligible players drafted.'], overall: 0,
    };
  }

  const talent = avg(players.map((pl) => TIER_TALENT[pl.tier]));
  const creation = Math.max(...players.map((pl) => pl.ratings.creation)) * 0.6 +
    avg(players.map((pl) => pl.ratings.creation)) * 0.4;
  const spacing = avg(players.map((pl) => pl.ratings.shooting));
  const perimeterDefense = avg(players.map((pl) => pl.ratings.perimeterDefense));
  const rimProtection = Math.max(...players.map((pl) => pl.ratings.rimProtection)) * 0.7 +
    avg(players.map((pl) => pl.ratings.rimProtection)) * 0.3;
  const rebounding = avg(players.map((pl) => pl.ratings.rebounding));

  // Fit penalties from the build plan.
  let fitPenalty = 0;
  const fitNotes: string[] = [];

  const nonShooters = players.filter((pl) => pl.ratings.shooting < 45).length;
  if (nonShooters >= 3) {
    fitPenalty += 6;
    fitNotes.push(`${nonShooters} non-shooters cramp the spacing.`);
  }

  const ballDominant = players.filter((pl) => pl.ballDominance >= 75).length;
  if (ballDominant >= 3) {
    fitPenalty += 5;
    fitNotes.push(`${ballDominant} ball-dominant scorers fight over touches.`);
  }

  if (!players.some((pl) => pl.ratings.rimProtection >= 75)) {
    fitPenalty += 5;
    fitNotes.push('No true rim protector.');
  }

  if (!players.some((pl) => pl.ratings.creation >= 80)) {
    fitPenalty += 6;
    fitNotes.push('No primary shot creator for late-game offense.');
  }

  const wings = players.filter(
    (pl) =>
      pl.positions.some((pos) => pos === 'SF' || pos === 'SG' || pos === 'PF') &&
      pl.heightInches >= 78,
  ).length;
  if (wings === 0) {
    fitPenalty += 4;
    fitNotes.push('No wing size to match up in a playoff series.');
  }

  // Versatility eases the clog: only players locked into a single spot count.
  const pureCenters = players.filter((pl) => pl.positions.length === 1 && pl.positions[0] === 'C').length;
  if (pureCenters >= 3) {
    fitPenalty += 4;
    fitNotes.push(`${pureCenters} centers is a clogged frontcourt.`);
  }
  const pureGuards = players.filter((pl) => pl.positions.length === 1 && pl.positions[0] === 'PG').length;
  if (pureGuards >= 3) {
    fitPenalty += 3;
    fitNotes.push(`${pureGuards} point guards is an awkward rotation.`);
  }

  if (fitNotes.length === 0) fitNotes.push('Clean roles — the pieces fit.');

  const overall =
    talent * 0.34 +
    creation * 0.16 +
    spacing * 0.12 +
    perimeterDefense * 0.14 +
    rimProtection * 0.12 +
    rebounding * 0.12 -
    fitPenalty;

  return {
    talent: Math.round(talent),
    creation: Math.round(creation),
    spacing: Math.round(spacing),
    perimeterDefense: Math.round(perimeterDefense),
    rimProtection: Math.round(rimProtection),
    rebounding: Math.round(rebounding),
    fitPenalty,
    fitNotes,
    overall: Math.round(overall * 10) / 10,
  };
}

const CLOSE_NOTES = [
  '{star} hits a dagger three with 24 seconds left.',
  '{star} gets the final stop at the rim.',
  '{star} dominates the last two minutes.',
  '{star} takes over in the fourth with 14 straight points.',
  'A {loserStar} comeback falls one possession short.',
  '{star} seals it at the line after a late steal.',
  '{star} controls the glass down the stretch.',
  'A 12-0 run behind {star} breaks it open early in the fourth.',
];

const BLOWOUT_NOTES = [
  '{star} cruises — it is over by the third quarter.',
  '{loserName}’s squad never recovers from a 20-2 first-quarter run.',
  '{star} feasts on every mismatch in a wire-to-wire win.',
];

function bestPlayerName(playerIds: string[], rng: Rng): string {
  const players = playerIds.map((id) => PLAYER_BY_ID[id]).filter(Boolean) as Player[];
  if (players.length === 0) return 'The team';
  const topTier = Math.min(...players.map((pl) => pl.tier));
  return pickOne(rng, players.filter((pl) => pl.tier === topTier)).displayName;
}

export function simulateSeries(
  matchId: string,
  rosters: [string[], string[]],
  names: [string, string],
): SeriesResult {
  const rng = makeRng(`series:${matchId}`);
  const ratings: [TeamRatingBreakdown, TeamRatingBreakdown] = [
    rateRoster(rosters[0]),
    rateRoster(rosters[1]),
  ];

  const games: SimGame[] = [];
  const wins: [number, number] = [0, 0];
  let gameIndex = 1;

  while (wins[0] < 4 && wins[1] < 4) {
    // 2-2-1-1-1 home court to the better-rated roster.
    const better: 0 | 1 = ratings[0].overall >= ratings[1].overall ? 0 : 1;
    const pattern = [better, better, 1 - better, 1 - better, better, 1 - better, better];
    const homeSide = pattern[gameIndex - 1] as 0 | 1;

    const edge = ratings[0].overall - ratings[1].overall + (homeSide === 0 ? 2.5 : -2.5);
    const swing = (rng() - 0.5) * 26; // any team can steal one game
    const margin = Math.round(edge * 0.55 + swing);
    const winnerSide: 0 | 1 = margin >= 0 ? 0 : 1;

    const loserScore = randomInt(rng, 92, 116);
    const winnerScore = loserScore + Math.max(1, Math.min(28, Math.abs(margin) + randomInt(rng, 1, 6)));
    const scores: [number, number] = winnerSide === 0 ? [winnerScore, loserScore] : [loserScore, winnerScore];

    const blowout = winnerScore - loserScore >= 18;
    const template = pickOne(rng, blowout ? BLOWOUT_NOTES : CLOSE_NOTES);
    const closingNote = template
      .replace('{star}', bestPlayerName(rosters[winnerSide], rng))
      .replace('{loserStar}', bestPlayerName(rosters[1 - winnerSide], rng))
      .replace('{loserName}', names[1 - winnerSide]);

    games.push({ index: gameIndex, homeSide, scores, winnerSide, closingNote });
    wins[winnerSide]++;
    gameIndex++;
  }

  const winnerSide: 0 | 1 = wins[0] === 4 ? 0 : 1;

  // Series MVP: highest-impact player on the winning team, with a seeded
  // nudge so it is not always the same superstar.
  const winnerPlayers = rosters[winnerSide]
    .map((id) => PLAYER_BY_ID[id])
    .filter(Boolean) as Player[];
  let mvpPlayerId = winnerPlayers[0]?.id ?? '';
  let bestScore = -1;
  for (const pl of winnerPlayers) {
    const impact = TIER_TALENT[pl.tier] + pl.ratings.scoring * 0.3 + pl.ratings.creation * 0.2 + rng() * 14;
    if (impact > bestScore) {
      bestScore = impact;
      mvpPlayerId = pl.id;
    }
  }

  const whyRundown = buildWhyRundown(ratings, winnerSide, names);

  return { winnerSide, wins, games, mvpPlayerId, ratings, whyRundown };
}

function buildWhyRundown(
  ratings: [TeamRatingBreakdown, TeamRatingBreakdown],
  winnerSide: 0 | 1,
  names: [string, string],
): string[] {
  const w = ratings[winnerSide];
  const l = ratings[1 - winnerSide];
  const winnerName = names[winnerSide];
  const loserName = names[1 - winnerSide];
  const lines: string[] = [];

  const dims: [keyof TeamRatingBreakdown, string][] = [
    ['talent', 'raw talent'],
    ['creation', 'late-game shot creation'],
    ['spacing', 'shooting and spacing'],
    ['perimeterDefense', 'perimeter defense'],
    ['rimProtection', 'rim protection'],
    ['rebounding', 'rebounding'],
  ];
  const edges = dims
    .map(([key, label]) => ({ label, diff: (w[key] as number) - (l[key] as number) }))
    .sort((x, y) => y.diff - x.diff);

  for (const edge of edges.slice(0, 3)) {
    if (edge.diff > 1) lines.push(`${winnerName} had the edge in ${edge.label} (+${Math.round(edge.diff)}).`);
  }
  if (lines.length === 0) {
    lines.push(`Dead even on paper — ${winnerName} won the coin-flip moments.`);
  }
  if (w.fitPenalty < l.fitPenalty) {
    lines.push(`${loserName}'s fit issues cost them: ${l.fitNotes[0]}`);
  } else if (w.fitPenalty > l.fitPenalty) {
    lines.push(`${winnerName} won despite fit issues (${w.fitNotes[0]}) — talent carried it.`);
  }
  return lines;
}
