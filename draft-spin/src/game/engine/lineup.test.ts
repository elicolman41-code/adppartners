import { describe, expect, it } from 'vitest';
import { buildLineup } from './lineup';
import { PLAYER_BY_ID } from '../data/db';

describe('multi-position data', () => {
  it('LeBron can play all five positions', () => {
    expect(PLAYER_BY_ID['lebron-james'].positions).toEqual(['SF', 'PG', 'SG', 'PF', 'C']);
  });
  it('Tim Duncan is a power forward or center', () => {
    expect(PLAYER_BY_ID['tim-duncan'].positions).toEqual(['PF', 'C']);
  });
});

describe('buildLineup', () => {
  it('slots five one-position players straight in', () => {
    const l = buildLineup(['john-stockton', 'reggie-miller', 'julius-erving', 'karl-malone', 'patrick-ewing']);
    expect(l.slots.PG).toBe('john-stockton');
    expect(l.slots.SG).toBe('reggie-miller');
    expect(l.slots.SF).toBe('julius-erving');
    expect(l.slots.PF).toBe('karl-malone');
    expect(l.slots.C).toBe('patrick-ewing');
    expect(l.bench).toHaveLength(0);
  });

  it('slides multi-position players to fill every slot', () => {
    // Two "SG" primaries + Duncan/KG bigs + LeBron: solvable only via flexibility.
    const l = buildLineup(['michael-jordan', 'kobe-bryant', 'tim-duncan', 'kevin-garnett', 'lebron-james']);
    const filled = Object.values(l.slots).filter(Boolean);
    expect(filled).toHaveLength(5);
    expect(l.bench).toHaveLength(0);
    // MJ or Kobe covers SG, the other slides to SF, LeBron takes PG.
    expect(l.slots.PG).toBe('lebron-james');
  });

  it('benches the extra player when a slot is truly contested', () => {
    const l = buildLineup(['john-stockton', 'steve-nash', 'chris-paul']);
    const filled = Object.values(l.slots).filter(Boolean);
    expect(filled).toHaveLength(1); // all three are pure PGs
    expect(l.bench).toHaveLength(2);
  });

  it('handles partial rosters (X-outs) with open slots', () => {
    const l = buildLineup(['nikola-jokic']);
    expect(l.slots.C).toBe('nikola-jokic');
    expect(l.slots.PG).toBeNull();
    expect(l.bench).toHaveLength(0);
  });
});
