import { describe, expect, it } from 'vitest';
import type { Match } from '../types';
import { aiOnClock, aiPickName } from './ai';
import { continueAfterReveal, createMatch, rematch, spinForRound, submitPick, unavailableIds } from './match';
import { resolvePlayer } from './search';
import { VALIDATORS } from './validators';
import { PLAYERS } from '../data/db';

function aiMatch(level: 'rookie' | 'veteran' | 'goat'): Match {
  return { ...spinForRound(createMatch('You', 'Bot', level)).match, turn: 1 as const };
}

describe('AI opponent', () => {
  it('createMatch seats an AI and rematch keeps it', () => {
    const m = createMatch('You', 'GOAT Bot', 'goat');
    expect(m.participants[1].ai).toBe('goat');
    expect(m.participants[0].ai).toBeUndefined();
    const g2 = rematch(m, 0);
    expect(g2.participants[1].ai).toBe('goat');
  });

  it('aiOnClock only fires for an AI seat in pick phase', () => {
    const human = spinForRound(createMatch('A', 'B')).match;
    expect(aiOnClock(human)).toBeNull();
    const bot = aiMatch('veteran');
    expect(bot.turn).toBe(1);
    expect(aiOnClock(bot)).toBe('veteran');
    expect(aiOnClock({ ...bot, phase: 'reveal' })).toBeNull();
  });

  it('picks are deterministic for the same match state', () => {
    const m = aiMatch('veteran');
    expect(aiPickName(m, 'veteran')).toBe(aiPickName(m, 'veteran'));
  });

  it('always returns a resolvable player name', () => {
    for (const level of ['rookie', 'veteran', 'goat'] as const) {
      const m = aiMatch(level);
      expect(resolvePlayer(aiPickName(m, level))).not.toBeNull();
    }
  });

  it('the GOAT never misses: every pick is eligible', () => {
    const m = aiMatch('goat');
    const cat = m.rounds[0].category;
    const fn = VALIDATORS[cat.validatorKey];
    const player = resolvePlayer(aiPickName(m, 'goat'))!;
    expect(fn(player, cat.params).eligible).toBe(true);
  });

  it('plays a full game against the GOAT bot to results with 5/5 rosters', () => {
    let m = createMatch('You', 'GOAT Bot', 'goat');
    for (let round = 0; round < m.totalRounds; round++) {
      m = spinForRound(m).match;
      let guard = 0;
      while (m.phase === 'pick') {
        if (++guard > 40) throw new Error('round never completed');
        const isAi = m.participants[m.turn].ai;
        const name = isAi ? aiPickName(m, isAi) : humanEligible(m);
        const out = submitPick(m, name);
        if (out.kind !== 'ruled') throw new Error('expected ruling');
        m = continueAfterReveal(out.match);
      }
    }
    expect(m.phase).toBe('results');
    expect(m.participants[0].roster).toHaveLength(5);
    expect(m.participants[1].roster).toHaveLength(5);
  });
});

function humanEligible(m: Match): string {
  const cat = m.rounds[m.currentRound].category;
  const fn = VALIDATORS[cat.validatorKey];
  const gone = unavailableIds(m);
  for (const a of m.rounds[m.currentRound].attempts) gone.add(a.pick.playerId);
  const found = PLAYERS.find((pl) => !gone.has(pl.id) && fn(pl, cat.params).eligible);
  if (!found) throw new Error(`no eligible player for ${cat.label}`);
  return found.displayName;
}
