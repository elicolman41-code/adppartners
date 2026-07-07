import type { Match, Pick, SpunCategory, ValidationResult } from '../types';
import { makeRng } from './rng';
import { spinCategory } from './categoryGen';
import { validatePick } from './validators';
import { resolvePlayer } from './search';
import { PLAYER_BY_ID, latestTeamId } from '../data/db';
import { playableCategoryCount } from './categoryGen';

export const TOTAL_ROUNDS = 5;

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
      { id: 'p1', name: youName || 'You', roster: [] },
      { id: 'p2', name: friendName || 'Friend', roster: [] },
    ],
    rounds: [],
    currentRound: 0,
    turn: 0,
    phase: 'spin',
    usedCategoryIds: [],
    game: 1,
    excludedIds: [],
    runWins: [0, 0],
  };
}

/**
 * Run it back: next game in the chain. Same two players, fresh categories,
 * and every player drafted so far in this run is out of the pool for both
 * sides. The winner of the game that just ended gets a run win.
 */
export function rematch(prev: Match, winnerSide: 0 | 1): Match {
  const base = createMatch(prev.participants[0].name, prev.participants[1].name);
  return {
    ...base,
    game: prev.game + 1,
    excludedIds: [...unavailableIds(prev)],
    runWins: runWinsAfter(prev, winnerSide),
  };
}

/** Run scoreboard once this game's winner is counted (shared by Results and rematch). */
export function runWinsAfter(match: Match, winnerSide: 0 | 1): [number, number] {
  return [
    match.runWins[0] + (winnerSide === 0 ? 1 : 0),
    match.runWins[1] + (winnerSide === 1 ? 1 : 0),
  ];
}

/**
 * Whether another chained game is winnable: a full match needs 5 distinct
 * playable categories against the pool that survives this game's drafting.
 */
export function canRunItBack(match: Match): boolean {
  return playableCategoryCount(unavailableIds(match)) >= match.totalRounds;
}

/** Every player id unavailable this match: drafted this game or in an earlier game of the run. */
export function unavailableIds(match: Match): Set<string> {
  return new Set([
    ...match.excludedIds,
    ...match.participants[0].roster,
    ...match.participants[1].roster,
  ]);
}

/** Spin the category for the current round (deterministic per match+round). */
export function spinForRound(match: Match): { match: Match; category: SpunCategory } {
  const rng = makeRng(`spin:${match.id}:round:${match.currentRound}`);
  const category = spinCategory(
    rng,
    match.usedCategoryIds,
    match.currentRound,
    match.totalRounds,
    unavailableIds(match),
  );
  const rounds = [...match.rounds];
  rounds[match.currentRound] = { index: match.currentRound, category, attempts: [] };
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

/** Whether a side has locked an eligible pick this round. */
export function hasLanded(match: Match, roundIndex: number, side: 0 | 1): boolean {
  const round = match.rounds[roundIndex];
  if (!round) return false;
  const pid = match.participants[side].id;
  return round.attempts.some((a) => a.participantId === pid && a.pick.outcome === 'eligible');
}

export type SubmitOutcome =
  | { kind: 'unknown'; input: string }
  | { kind: 'ruled'; result: ValidationResult; pick: Pick; match: Match };

/**
 * Submit a typed pick for the participant whose turn it is.
 * - Unknown/typo: no state change — retry freely.
 * - Eligible: locks into the roster; that side is done for the round.
 * - Ineligible or duplicate: crossed out (X) and the turn passes to the
 *   other player on the same category (or back to you if they're already
 *   done). Nobody loses a roster spot — both sides always land five.
 */
export function submitPick(match: Match, input: string): SubmitOutcome {
  const player = resolvePlayer(input);
  if (!player) return { kind: 'unknown', input };

  // Defensive: never let an already-landed side pick again (e.g. a tampered
  // or corrupted save) — hand the clock to the side that still needs one.
  if (
    hasLanded(match, match.currentRound, match.turn) &&
    !hasLanded(match, match.currentRound, (1 - match.turn) as 0 | 1)
  ) {
    match = { ...match, turn: (1 - match.turn) as 0 | 1 };
  }

  const round = match.rounds[match.currentRound];
  const category = round.category;
  const participant = match.participants[match.turn];

  const usedEarlierGame = match.excludedIds.includes(player.id);
  const draftedThisGame = match.participants.some((pt) => pt.roster.includes(player.id));
  const crossedOutThisRound = round.attempts.some((a) => a.pick.playerId === player.id);

  let pick: Pick;
  let result: ValidationResult;

  if (usedEarlierGame || draftedThisGame || crossedOutThisRound) {
    const reason = usedEarlierGame
      ? `${player.displayName} was drafted in an earlier game of this run — he's out of the pool. ✕, pass the turn.`
      : draftedThisGame
        ? `${player.displayName} has already been drafted this game. Duplicates are crossed out — the turn passes.`
        : `${player.displayName} was already crossed out this round — he can't be re-picked here. ✕, pass the turn.`;
    result = {
      eligible: false,
      reason,
      player: {
        id: player.id,
        displayName: player.displayName,
        positions: player.positions,
        team: latestTeamId(player),
      },
      evidence: [
        {
          field: 'Duplicate check',
          expected: usedEarlierGame
            ? 'not drafted earlier in this run'
            : draftedThisGame
              ? 'not yet drafted this game'
              : 'not already ruled on this round',
          actual: usedEarlierGame || draftedThisGame ? 'already drafted' : 'crossed out earlier this round',
          sourceNote: usedEarlierGame ? `Run history (game ${match.game} of the run)` : 'Match state',
        },
      ],
    };
    pick = { playerId: player.id, outcome: 'duplicate', reason: result.reason, evidence: result.evidence };
  } else {
    result = validatePick(player, category);
    pick = {
      playerId: player.id,
      outcome: result.eligible ? 'eligible' : 'ineligible',
      reason: result.reason,
      evidence: result.evidence,
    };
  }

  const participants = match.participants.map((pt, i) => {
    if (i !== match.turn) return pt;
    return {
      ...pt,
      roster: pick.outcome === 'eligible' ? [...pt.roster, pick.playerId] : pt.roster,
    };
  }) as Match['participants'];

  const rounds = [...match.rounds];
  rounds[match.currentRound] = {
    ...round,
    attempts: [...round.attempts, { participantId: participant.id, pick }],
  };

  const withPick: Match = { ...match, participants, rounds };

  // Turn order after a ruling: the other side goes if it still needs a pick
  // (normal alternation AND the steal after an X); otherwise you keep the
  // clock until you land one.
  const other = (1 - match.turn) as 0 | 1;
  const nextTurn = !hasLanded(withPick, match.currentRound, other) ? other : match.turn;

  const next: Match = { ...withPick, turn: nextTurn, phase: 'reveal' };

  return { kind: 'ruled', result, pick, match: next };
}

/** Whether both sides have locked an eligible pick this round. */
export function roundComplete(match: Match, roundIndex: number): boolean {
  return hasLanded(match, roundIndex, 0) && hasLanded(match, roundIndex, 1);
}

/** Advance after the reveal screen. */
export function continueAfterReveal(match: Match): Match {
  if (!roundComplete(match, match.currentRound)) {
    return { ...match, phase: 'pick' }; // same category, next picker (turn already set)
  }
  const isLastRound = match.currentRound === match.totalRounds - 1;
  if (isLastRound) {
    return { ...match, phase: 'results' };
  }
  return { ...match, currentRound: match.currentRound + 1, phase: 'spin', turn: 0 };
}

export function rosterNames(match: Match, side: 0 | 1): string[] {
  return match.participants[side].roster.map((id) => PLAYER_BY_ID[id]?.displayName ?? id);
}

export interface RoundMark {
  /** Eligible pick locked this round. */
  landed: boolean;
  /** Crossed-out attempts before (or without) landing. */
  misses: number;
  /** The round has been spun. */
  played: boolean;
}

/** Per-round marks for a participant, for the score strip. */
export function roundMarks(match: Match, side: 0 | 1): RoundMark[] {
  const pid = match.participants[side].id;
  return Array.from({ length: match.totalRounds }, (_, i) => {
    const round = match.rounds[i];
    if (!round) return { landed: false, misses: 0, played: false };
    const mine = round.attempts.filter((a) => a.participantId === pid);
    return {
      landed: mine.some((a) => a.pick.outcome === 'eligible'),
      misses: mine.filter((a) => a.pick.outcome !== 'eligible').length,
      played: true,
    };
  });
}

// ---------------------------------------------------------------------------
// Persistence — reloading the room restores the match (and the seeded
// simulation reproduces the identical series result).
// ---------------------------------------------------------------------------

const STORAGE_KEY = 'draft-spin-match-v3';

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
    localStorage.removeItem('draft-spin-match-v2'); // pre-steal-rule schema, unreadable now
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as Match;
    if (!parsed || !Array.isArray(parsed.rounds) || parsed.participants?.length !== 2) return null;
    if (typeof parsed.game !== 'number' || !Array.isArray(parsed.excludedIds)) return null;
    if (!Array.isArray(parsed.runWins) || parsed.runWins.length !== 2) return null;
    if (!parsed.rounds.every((r) => r && Array.isArray(r.attempts))) return null;
    return parsed;
  } catch {
    return null;
  }
}
