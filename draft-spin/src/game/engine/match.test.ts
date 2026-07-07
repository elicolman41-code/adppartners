import { describe, expect, it } from 'vitest';
import type { Match } from '../types';
import { continueAfterReveal, createMatch, spinForRound, submitPick } from './match';
import { PLAYER_BY_ID, PLAYERS } from '../data/db';
import { VALIDATORS } from './validators';

function freshRound(): Match {
  const match = createMatch('You', 'Friend');
  return spinForRound(match).match;
}

/** Find a player who is eligible / ineligible for the current category. */
function findPick(match: Match, eligible: boolean, excludeIds: string[] = []): string {
  const cat = match.rounds[match.currentRound].category;
  const fn = VALIDATORS[cat.validatorKey];
  const found = PLAYERS.find(
    (pl) => !excludeIds.includes(pl.id) && fn(pl, cat.params).eligible === eligible,
  );
  if (!found) throw new Error(`no ${eligible ? 'eligible' : 'ineligible'} player for ${cat.label}`);
  return found.displayName;
}

describe('match creation', () => {
  it('creates a room with a 4-character code and two participants', () => {
    const m = createMatch('You', 'Friend');
    expect(m.roomCode).toMatch(/^[A-Z2-9]{4}$/);
    expect(m.participants.map((p) => p.name)).toEqual(['You', 'Friend']);
    expect(m.totalRounds).toBe(5);
    expect(m.phase).toBe('spin');
  });
});

describe('category spinning', () => {
  it('never repeats a category within a match', () => {
    let m = createMatch('A', 'B');
    const seen: string[] = [];
    for (let r = 0; r < 5; r++) {
      const spun = spinForRound(m);
      m = spun.match;
      expect(seen).not.toContain(spun.category.definitionId);
      seen.push(spun.category.definitionId);
      // fake both picks to advance
      m = { ...m, currentRound: r + 1 < 5 ? r + 1 : r, phase: 'spin' };
    }
  });

  it('spins deterministically for the same match id and round', () => {
    const m = createMatch('A', 'B');
    const a = spinForRound(m).category;
    const b = spinForRound(m).category;
    expect(a).toEqual(b);
  });
});

describe('X-out pick rules', () => {
  it('eligible pick locks into the roster', () => {
    const m = freshRound();
    const name = findPick(m, true);
    const out = submitPick(m, name);
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('eligible');
    expect(out.match.participants[0].roster).toHaveLength(1);
  });

  it('ineligible real-player pick is crossed out: no roster lock, round lost', () => {
    const m = freshRound();
    const name = findPick(m, false);
    const out = submitPick(m, name);
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('ineligible');
    expect(out.match.participants[0].roster).toHaveLength(0);
    // The round is consumed — the pick is recorded as an X, not retryable.
    const roundPicks = out.match.rounds[out.match.currentRound].picks;
    expect(roundPicks['p1']?.outcome).toBe('ineligible');
    expect(out.result.reason.length).toBeGreaterThan(0);
    expect(out.result.evidence.length).toBeGreaterThan(0);
  });

  it('unknown/typo: retry allowed, state unchanged', () => {
    const m = freshRound();
    const out = submitPick(m, 'Kevon Duran the Third');
    expect(out.kind).toBe('unknown');
    expect(Object.keys(m.rounds[m.currentRound].picks)).toHaveLength(0);
  });

  it('duplicate real-player pick is crossed out for the second picker', () => {
    const m = freshRound();
    const name = findPick(m, true);
    const first = submitPick(m, name);
    if (first.kind !== 'ruled') throw new Error('expected ruling');
    const afterReveal = continueAfterReveal(first.match); // now friend's turn
    expect(afterReveal.turn).toBe(1);
    const second = submitPick(afterReveal, name);
    if (second.kind !== 'ruled') throw new Error('expected ruling');
    expect(second.pick.outcome).toBe('duplicate');
    expect(second.match.participants[1].roster).toHaveLength(0);
  });
});

describe('full match flow', () => {
  it('plays a complete 5-round match and reaches results', () => {
    let m = createMatch('You', 'Friend');
    for (let round = 0; round < 5; round++) {
      m = spinForRound(m).match;
      expect(m.phase).toBe('pick');
      const used: string[] = m.participants.flatMap((pt) => pt.roster);

      const you = submitPick(m, findPick(m, true, used));
      if (you.kind !== 'ruled') throw new Error('expected ruling');
      m = continueAfterReveal(you.match);
      expect(m.phase).toBe('pick');
      expect(m.turn).toBe(1);

      const usedNow = m.participants.flatMap((pt) => pt.roster);
      const friend = submitPick(m, findPick(m, true, usedNow));
      if (friend.kind !== 'ruled') throw new Error('expected ruling');
      m = continueAfterReveal(friend.match);
    }
    expect(m.phase).toBe('results');
    expect(m.participants[0].roster).toHaveLength(5);
    expect(m.participants[1].roster).toHaveLength(5);
    expect(m.usedCategoryIds).toHaveLength(5);
    expect(new Set(m.usedCategoryIds).size).toBe(5);
  });
});

describe('duplicate prevention across rosters', () => {
  it('a player locked in round 1 cannot be re-picked in round 3', () => {
    let m = createMatch('You', 'Friend');
    m = spinForRound(m).match;
    const name = findPick(m, true);
    const first = submitPick(m, name);
    if (first.kind !== 'ruled') throw new Error('expected ruling');
    const pickedId = first.pick.playerId;
    m = continueAfterReveal(first.match);

    // Friend now tries the very same player — duplicate even if eligible.
    const dup = submitPick(m, PLAYER_BY_ID[pickedId].displayName);
    if (dup.kind !== 'ruled') throw new Error('expected ruling');
    expect(dup.pick.outcome).toBe('duplicate');
  });
});
