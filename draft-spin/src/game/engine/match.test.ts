import { describe, expect, it } from 'vitest';
import type { Match } from '../types';
import {
  canRunItBack,
  continueAfterReveal,
  createMatch,
  rematch,
  roundComplete,
  roundMarks,
  runWinsAfter,
  spinForRound,
  submitPick,
  unavailableIds,
} from './match';
import { playableCategoryCount } from './categoryGen';
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
  const gone = unavailableIds(match);
  const found = PLAYERS.find(
    (pl) =>
      !excludeIds.includes(pl.id) &&
      !gone.has(pl.id) &&
      fn(pl, cat.params).eligible === eligible,
  );
  if (!found) throw new Error(`no ${eligible ? 'eligible' : 'ineligible'} player for ${cat.label}`);
  return found.displayName;
}

/** Land an eligible pick for whoever's turn it is; return the advanced match. */
function landPick(m: Match): Match {
  const out = submitPick(m, findPick(m, true));
  if (out.kind !== 'ruled') throw new Error('expected ruling');
  return continueAfterReveal(out.match);
}

/** Play a full game to results, everyone picking eligible players. */
function playFullGame(m: Match): Match {
  for (let round = 0; round < m.totalRounds; round++) {
    m = spinForRound(m).match;
    while (m.phase === 'pick') m = landPick(m);
  }
  return m;
}

describe('match creation', () => {
  it('creates a room with a 4-character code, two participants, game 1 of a fresh run', () => {
    const m = createMatch('You', 'Friend');
    expect(m.roomCode).toMatch(/^[A-Z2-9]{4}$/);
    expect(m.participants.map((p) => p.name)).toEqual(['You', 'Friend']);
    expect(m.totalRounds).toBe(5);
    expect(m.phase).toBe('spin');
    expect(m.game).toBe(1);
    expect(m.excludedIds).toEqual([]);
    expect(m.runWins).toEqual([0, 0]);
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

describe('steal rule: an X passes the turn on the same category', () => {
  it('eligible pick locks into the roster and hands the turn over', () => {
    const m = freshRound();
    const out = submitPick(m, findPick(m, true));
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('eligible');
    expect(out.match.participants[0].roster).toHaveLength(1);
    expect(out.match.turn).toBe(1);
  });

  it('ineligible pick is crossed out, the round is NOT lost, other player is up', () => {
    const m = freshRound();
    const out = submitPick(m, findPick(m, false));
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('ineligible');
    expect(out.match.participants[0].roster).toHaveLength(0);
    expect(out.match.turn).toBe(1); // steal — same category, other player
    const after = continueAfterReveal(out.match);
    expect(after.phase).toBe('pick'); // same round continues
    expect(after.currentRound).toBe(m.currentRound);
    expect(out.result.reason.length).toBeGreaterThan(0);
    expect(out.result.evidence.length).toBeGreaterThan(0);
  });

  it('after a miss you get the turn back once the other player lands', () => {
    let m = freshRound();
    // P1 misses -> P2 up on same category.
    let out = submitPick(m, findPick(m, false));
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    m = continueAfterReveal(out.match);
    expect(m.turn).toBe(1);
    // P2 lands -> back to P1, still same category.
    out = submitPick(m, findPick(m, true));
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('eligible');
    m = continueAfterReveal(out.match);
    expect(m.phase).toBe('pick');
    expect(m.turn).toBe(0);
    // P1 finally lands -> round complete.
    out = submitPick(m, findPick(m, true));
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(roundComplete(out.match, out.match.currentRound)).toBe(true);
    expect(out.match.participants[0].roster).toHaveLength(1);
    expect(out.match.participants[1].roster).toHaveLength(1);
  });

  it('keeps the clock on you when the other player already landed', () => {
    let m = freshRound();
    m = landPick(m); // P1 lands, P2 up
    const miss = submitPick(m, findPick(m, false));
    if (miss.kind !== 'ruled') throw new Error('expected ruling');
    // P2 missed but P1 is done — P2 stays on the clock.
    expect(miss.match.turn).toBe(1);
    const after = continueAfterReveal(miss.match);
    expect(after.phase).toBe('pick');
    expect(after.turn).toBe(1);
  });

  it('unknown/typo: retry allowed, state unchanged', () => {
    const m = freshRound();
    const out = submitPick(m, 'Kevon Duran the Third');
    expect(out.kind).toBe('unknown');
    expect(m.rounds[m.currentRound].attempts).toHaveLength(0);
  });

  it('duplicate real-player pick is crossed out and passes the turn', () => {
    let m = freshRound();
    const name = findPick(m, true);
    const first = submitPick(m, name);
    if (first.kind !== 'ruled') throw new Error('expected ruling');
    m = continueAfterReveal(first.match);
    expect(m.turn).toBe(1);
    const second = submitPick(m, name);
    if (second.kind !== 'ruled') throw new Error('expected ruling');
    expect(second.pick.outcome).toBe('duplicate');
    expect(second.match.participants[1].roster).toHaveLength(0);
    // P1 already landed, so P2 keeps trying.
    expect(second.match.turn).toBe(1);
  });

  it('a player crossed out this round cannot be re-picked in the same round', () => {
    let m = freshRound();
    const badName = findPick(m, false);
    let out = submitPick(m, badName); // P1 X
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    m = continueAfterReveal(out.match); // steal: P2 up
    out = submitPick(m, badName); // P2 tries the crossed-out player
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('duplicate');
    expect(out.pick.reason).toContain('crossed out this round');
  });

  it('roundMarks count misses and still show a landed round as a hit', () => {
    let m = freshRound();
    let out = submitPick(m, findPick(m, false)); // P1 miss
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    m = continueAfterReveal(out.match); // P2 up
    out = submitPick(m, findPick(m, true)); // P2 lands
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    m = continueAfterReveal(out.match); // back to P1
    out = submitPick(m, findPick(m, true)); // P1 lands
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    const marksP1 = roundMarks(out.match, 0)[0];
    expect(marksP1).toEqual({ landed: true, misses: 1, played: true });
    const marksP2 = roundMarks(out.match, 1)[0];
    expect(marksP2).toEqual({ landed: true, misses: 0, played: true });
  });
});

describe('full match flow', () => {
  it('plays a complete 5-round match — both sides always end with five', () => {
    let m = createMatch('You', 'Friend');
    m = playFullGame(m);
    expect(m.phase).toBe('results');
    expect(m.participants[0].roster).toHaveLength(5);
    expect(m.participants[1].roster).toHaveLength(5);
    expect(m.usedCategoryIds).toHaveLength(5);
    expect(new Set(m.usedCategoryIds).size).toBe(5);
  });

  it('both sides end with five even through misses', () => {
    let m = createMatch('You', 'Friend');
    for (let round = 0; round < m.totalRounds; round++) {
      m = spinForRound(m).match;
      let missed = false;
      while (m.phase === 'pick') {
        // First attempt of each round is a deliberate miss.
        const wantEligible = missed || m.rounds[m.currentRound].attempts.length > 0;
        const out = submitPick(m, findPick(m, wantEligible ? true : false));
        if (out.kind !== 'ruled') throw new Error('expected ruling');
        missed = true;
        m = continueAfterReveal(out.match);
      }
    }
    expect(m.phase).toBe('results');
    expect(m.participants[0].roster).toHaveLength(5);
    expect(m.participants[1].roster).toHaveLength(5);
    const totalMisses = [0, 1]
      .flatMap((s) => roundMarks(m, s as 0 | 1))
      .reduce((n, mk) => n + mk.misses, 0);
    expect(totalMisses).toBe(5); // one deliberate miss per round
  });
});

describe('run it back', () => {
  it('chains a new game with drafted players excluded and run wins tallied', () => {
    let g1 = createMatch('You', 'Friend');
    g1 = playFullGame(g1);
    const drafted = [...g1.participants[0].roster, ...g1.participants[1].roster];
    expect(drafted).toHaveLength(10);

    const g2 = rematch(g1, 0);
    expect(g2.game).toBe(2);
    expect(g2.runWins).toEqual([1, 0]);
    expect(g2.id).not.toBe(g1.id);
    expect(new Set(g2.excludedIds)).toEqual(new Set(drafted));
    expect(g2.participants[0].roster).toEqual([]);
    expect(g2.participants[1].name).toBe('Friend');
  });

  it('a player drafted in an earlier game is crossed out in the next one', () => {
    let g1 = createMatch('You', 'Friend');
    g1 = playFullGame(g1);
    const usedId = g1.participants[0].roster[0];

    let g2 = rematch(g1, 1);
    g2 = spinForRound(g2).match;
    const out = submitPick(g2, PLAYER_BY_ID[usedId].displayName);
    if (out.kind !== 'ruled') throw new Error('expected ruling');
    expect(out.pick.outcome).toBe('duplicate');
    expect(out.pick.reason).toContain('earlier game');
    expect(out.match.participants[0].roster).toHaveLength(0);
  });

  it('runWinsAfter is the single source of the run tally', () => {
    const m = { ...createMatch('A', 'B'), runWins: [2, 1] as [number, number] };
    expect(runWinsAfter(m, 0)).toEqual([3, 1]);
    expect(runWinsAfter(m, 1)).toEqual([2, 2]);
  });

  it('the run ends gracefully when the pool is drafted out', () => {
    // Full pool: every category playable, run-it-back on.
    expect(playableCategoryCount(new Set())).toBeGreaterThanOrEqual(25);
    expect(canRunItBack(createMatch('A', 'B'))).toBe(true);
    // Pool emptied: nothing playable, run-it-back gated off.
    expect(playableCategoryCount(new Set(PLAYERS.map((p) => p.id)))).toBe(0);
    const drained = { ...createMatch('A', 'B'), excludedIds: PLAYERS.map((p) => p.id) };
    expect(canRunItBack(drained)).toBe(false);
  });

  it('survives a long run: five chained games, no repeats anywhere', () => {
    let m = createMatch('You', 'Friend');
    const everDrafted = new Set<string>();
    for (let game = 0; game < 5; game++) {
      m = playFullGame(m);
      for (const pt of m.participants) {
        for (const id of pt.roster) {
          expect(everDrafted.has(id), `player ${id} drafted twice in the run`).toBe(false);
          everDrafted.add(id);
        }
      }
      m = rematch(m, game % 2 === 0 ? 0 : 1);
    }
    expect(everDrafted.size).toBe(50);
    expect(m.game).toBe(6);
    expect(m.runWins[0] + m.runWins[1]).toBe(5);
  });
});
