import type { Match, Pick, SpunCategory, ValidationResult } from '../types';
import { makeRng } from './rng';
import { spinCategory } from './categoryGen';
import { validatePick } from './validators';
import { resolvePlayer } from './search';
import { PLAYER_BY_ID } from '../data/db';

export const TOTAL_ROUNDS = 5;
export const WIN_SERIES_BONUS = 3;

function makeRoomCode(rng: () => number): string {
  const letters = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 4; i++) code += letters[Math.floor(rng() * letters.length)];
  return code;
}

export function createMatch(youName: string, friendName: string): Match {
  const id = `m-${Date.now().toString(36)}-${Math.floor(Math.random() * 1e6).toString(36)}`;
  const rng = makeRng(`room:${id}`);
  return {
    id,
    roomCode: makeRoomCode(rng),
    createdAt: Date.now(),
    totalRounds: TOTAL_ROUNDS,
    participants: [
      { id: 'p1', name: youName || 'You', score: 0, roster: [] },
      { id: 'p2', name: friendName || 'Friend', score: 0, roster: [] },
    ],
    rounds: [],
    currentRound: 0,
    turn: 0,
    phase: 'spin',
    usedCategoryIds: [],
  };
}

/** Spin the category for the current round (deterministic per match+round). */
export function spinForRound(match: Match): { match: Match; category: SpunCategory } {
  const rng = makeRng(`spin:${match.id}:round:${match.currentRound}`);
  const category = spinCategory(rng, match.usedCategoryIds, match.currentRound, match.totalRounds);
  const rounds = [...match.rounds];
  rounds[match.currentRound] = { index: match.currentRound, category, picks: {} };
  return {
    match: {
      ...match,
      rounds,
      usedCategoryIds: [...match.usedCategoryIds, category.definitionId],
      phase: 'pick',
      turn: 0,
    },
    category,
  };
}

export type SubmitOutcome =
  | { kind: 'unknown'; input: string }
  | { kind: 'ruled'; result: ValidationResult; pick: Pick; match: Match };

/**
 * Submit a typed pick for the participant whose turn it is.
 * - Unknown/typo: no penalty, no state change — retry.
 * - Duplicate real player (either roster or same round): -1.
 * - Eligible: +1 and lock into roster.  Ineligible: -1 with reason.
 */
export function submitPick(match: Match, input: string): SubmitOutcome {
  const player = resolvePlayer(input);
  if (!player) return { kind: 'unknown', input };

  const round = match.rounds[match.currentRound];
  const category = round.category;
  const participant = match.participants[match.turn];

  const alreadyPicked =
    match.participants.some((pt) => pt.roster.includes(player.id)) ||
    Object.values(round.picks).some((pk) => pk && pk.playerId === player.id);

  let pick: Pick;
  let result: ValidationResult;

  if (alreadyPicked) {
    result = {
      eligible: false,
      reason: `${player.displayName} has already been drafted this match. Duplicate picks lose a point.`,
      penalty: -1,
      player: {
        id: player.id,
        displayName: player.displayName,
        position: player.position,
        team: player.seasons[player.seasons.length - 1]?.teamId ?? '',
      },
      evidence: [
        {
          field: 'Duplicate check',
          expected: 'not yet drafted in this match',
          actual: 'already drafted',
          sourceNote: 'Match state',
        },
      ],
    };
    pick = { playerId: player.id, outcome: 'duplicate', points: -1, reason: result.reason, evidence: result.evidence };
  } else {
    result = validatePick(player, category);
    pick = {
      playerId: player.id,
      outcome: result.eligible ? 'eligible' : 'ineligible',
      points: result.eligible ? 1 : -1,
      reason: result.reason,
      evidence: result.evidence,
    };
  }

  const participants = match.participants.map((pt, i) => {
    if (i !== match.turn) return pt;
    return {
      ...pt,
      score: pt.score + pick.points,
      roster: pick.outcome === 'eligible' ? [...pt.roster, pick.playerId] : pt.roster,
    };
  }) as Match['participants'];

  const rounds = [...match.rounds];
  rounds[match.currentRound] = {
    ...round,
    picks: { ...round.picks, [participant.id]: pick },
  };

  const bothPicked = Object.keys(rounds[match.currentRound].picks).length === 2;

  // currentRound advances when the reveal screen is dismissed, not here.
  const next: Match = {
    ...match,
    participants,
    rounds,
    turn: bothPicked ? 0 : ((1 - match.turn) as 0 | 1),
    phase: 'reveal',
  };

  return { kind: 'ruled', result, pick, match: next };
}

/** Advance after the reveal screen. */
export function continueAfterReveal(match: Match): Match {
  const round = match.rounds[match.currentRound];
  const bothPicked = Object.keys(round.picks).length === 2;

  if (!bothPicked) {
    return { ...match, phase: 'pick' }; // other player's turn in same round
  }
  const isLastRound = match.currentRound === match.totalRounds - 1;
  if (isLastRound) {
    return { ...match, phase: 'results' };
  }
  return { ...match, currentRound: match.currentRound + 1, phase: 'spin', turn: 0 };
}

/** Apply the optional +3 series-win bonus once results are simulated. */
export function applySeriesBonus(match: Match, winnerSide: 0 | 1): Match {
  const participants = match.participants.map((pt, i) =>
    i === winnerSide ? { ...pt, score: pt.score + WIN_SERIES_BONUS } : pt,
  ) as Match['participants'];
  return { ...match, participants };
}

export function rosterNames(match: Match, side: 0 | 1): string[] {
  return match.participants[side].roster.map((id) => PLAYER_BY_ID[id]?.displayName ?? id);
}

// ---------------------------------------------------------------------------
// Persistence — reloading the room restores the match (and the seeded
// simulation reproduces the identical series result).
// ---------------------------------------------------------------------------

const STORAGE_KEY = 'draft-spin-match-v1';

export function saveMatch(match: Match | null): void {
  try {
    if (match === null) localStorage.removeItem(STORAGE_KEY);
    else localStorage.setItem(STORAGE_KEY, JSON.stringify(match));
  } catch {
    // Private mode etc. — the game still works, it just won't survive reload.
  }
}

export function loadMatch(): Match | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Match;
    if (!parsed || !Array.isArray(parsed.rounds) || parsed.participants?.length !== 2) return null;
    return parsed;
  } catch {
    return null;
  }
}
