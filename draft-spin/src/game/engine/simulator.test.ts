import { describe, expect, it } from 'vitest';
import { rateRoster, simulateSeries } from './simulator';

const SUPER_TEAM = ['michael-jordan', 'lebron-james', 'stephen-curry', 'tim-duncan', 'hakeem-olajuwon'];
const ROLE_TEAM = ['muggsy-bogues', 'derek-fisher', 'bruce-bowen', 'udonis-haslem', 'boban-marjanovic'];
const BALANCED_TEAM = ['chris-paul', 'klay-thompson', 'kawhi-leonard', 'kevin-garnett', 'rudy-gobert'];

describe('rateRoster', () => {
  it('rates a superteam far above a role-player team', () => {
    const superRating = rateRoster(SUPER_TEAM);
    const roleRating = rateRoster(ROLE_TEAM);
    expect(superRating.overall).toBeGreaterThan(roleRating.overall + 15);
  });

  it('flags fit problems: no creator and no rim protector', () => {
    const rating = rateRoster(['bruce-bowen', 'tony-allen', 'duncan-robinson', 'buddy-hield', 'shane-battier']);
    expect(rating.fitPenalty).toBeGreaterThan(0);
    expect(rating.fitNotes.join(' ')).toContain('rim protector');
    expect(rating.fitNotes.join(' ')).toContain('shot creator');
  });

  it('flags too many ball-dominant scorers', () => {
    const rating = rateRoster(['allen-iverson', 'james-harden', 'luka-doncic', 'trae-young', 'russell-westbrook']);
    expect(rating.fitNotes.join(' ')).toContain('ball-dominant');
  });

  it('gives clean-fit note when roles are clear', () => {
    const rating = rateRoster(BALANCED_TEAM);
    expect(rating.fitPenalty).toBe(0);
    expect(rating.fitNotes[0]).toContain('fit');
  });

  it('handles an empty roster without crashing', () => {
    const rating = rateRoster([]);
    expect(rating.overall).toBe(0);
  });
});

describe('simulateSeries', () => {
  it('is deterministic: same match id twice gives the identical series', () => {
    const a = simulateSeries('match-123', [SUPER_TEAM, BALANCED_TEAM], ['You', 'Friend']);
    const b = simulateSeries('match-123', [SUPER_TEAM, BALANCED_TEAM], ['You', 'Friend']);
    expect(a).toEqual(b);
  });

  it('different match ids can differ (seeded by match id)', () => {
    const results = new Set<string>();
    for (let i = 0; i < 12; i++) {
      const r = simulateSeries(`match-${i}`, [BALANCED_TEAM, SUPER_TEAM], ['You', 'Friend']);
      results.add(`${r.wins[0]}-${r.wins[1]}`);
    }
    expect(results.size).toBeGreaterThan(1);
  });

  it('produces a valid best-of-7: winner has exactly 4 wins, 4-7 games', () => {
    const r = simulateSeries('match-check', [SUPER_TEAM, BALANCED_TEAM], ['You', 'Friend']);
    expect(r.wins[r.winnerSide]).toBe(4);
    expect(r.wins[1 - r.winnerSide]).toBeLessThan(4);
    expect(r.games.length).toBeGreaterThanOrEqual(4);
    expect(r.games.length).toBeLessThanOrEqual(7);
    expect(r.games.length).toBe(r.wins[0] + r.wins[1]);
  });

  it('every game has plausible scores and a closing note', () => {
    const r = simulateSeries('match-notes', [SUPER_TEAM, ROLE_TEAM], ['You', 'Friend']);
    for (const g of r.games) {
      const [s0, s1] = g.scores;
      expect(Math.max(s0, s1)).toBeLessThanOrEqual(150);
      expect(Math.min(s0, s1)).toBeGreaterThanOrEqual(85);
      expect(s0).not.toBe(s1);
      expect(g.scores[g.winnerSide]).toBeGreaterThan(g.scores[1 - g.winnerSide]);
      expect(g.closingNote.length).toBeGreaterThan(10);
      expect(g.closingNote).not.toContain('{');
    }
  });

  it('superteam beats role players in the vast majority of seeds', () => {
    let superWins = 0;
    for (let i = 0; i < 30; i++) {
      const r = simulateSeries(`sweep-${i}`, [SUPER_TEAM, ROLE_TEAM], ['You', 'Friend']);
      if (r.winnerSide === 0) superWins++;
    }
    expect(superWins).toBeGreaterThanOrEqual(27);
  });

  it('names a series MVP from the winning roster', () => {
    const r = simulateSeries('match-mvp', [SUPER_TEAM, BALANCED_TEAM], ['You', 'Friend']);
    expect([...SUPER_TEAM, ...BALANCED_TEAM]).toContain(r.mvpPlayerId);
    const winningRoster = r.winnerSide === 0 ? SUPER_TEAM : BALANCED_TEAM;
    expect(winningRoster).toContain(r.mvpPlayerId);
  });

  it('explains why the winner won', () => {
    const r = simulateSeries('match-why', [SUPER_TEAM, ROLE_TEAM], ['You', 'Friend']);
    expect(r.whyRundown.length).toBeGreaterThan(0);
    for (const line of r.whyRundown) expect(line.length).toBeGreaterThan(10);
  });
});
