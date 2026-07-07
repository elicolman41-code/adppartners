import { describe, expect, it } from 'vitest';
import { PLAYERS } from './db';
import { TEAMS } from './teams';
import { POSITION_ORDER } from '../types';
import { normalizeName } from '../engine/search';

const TEAM_IDS = new Set(TEAMS.map((t) => t.id));

describe('seed data integrity', () => {
  it('has a healthy pool size', () => {
    expect(PLAYERS.length).toBeGreaterThanOrEqual(220);
  });

  it('player ids are unique', () => {
    const ids = PLAYERS.map((pl) => pl.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('every season stint references a real franchise id', () => {
    for (const pl of PLAYERS) {
      for (const s of pl.seasons) {
        expect(TEAM_IDS.has(s.teamId), `${pl.id}: unknown team ${s.teamId}`).toBe(true);
        expect(s.from, `${pl.id}: stint years inverted`).toBeLessThanOrEqual(s.to);
      }
    }
  });

  it('every position is one of PG/SG/SF/PF/C with no duplicates', () => {
    for (const pl of PLAYERS) {
      expect(pl.positions.length, `${pl.id}: no positions`).toBeGreaterThan(0);
      expect(new Set(pl.positions).size).toBe(pl.positions.length);
      for (const pos of pl.positions) {
        expect(POSITION_ORDER, `${pl.id}: bad position ${pos}`).toContain(pos);
      }
    }
  });

  it('no two players share a normalized name or alias (exact-submit is unambiguous)', () => {
    const seen = new Map<string, string>();
    const collisions: string[] = [];
    for (const pl of PLAYERS) {
      for (const key of [pl.displayName, ...pl.aliases].map(normalizeName)) {
        const other = seen.get(key);
        if (other && other !== pl.id) collisions.push(`"${key}": ${other} vs ${pl.id}`);
        seen.set(key, pl.id);
      }
    }
    expect(collisions).toEqual([]);
  });

  it('championships and awards are non-negative and sane', () => {
    for (const pl of PLAYERS) {
      expect(pl.championships).toBeGreaterThanOrEqual(0);
      expect(pl.championships).toBeLessThanOrEqual(11); // Bill Russell
      expect(pl.awards.allStar).toBeLessThanOrEqual(21); // LeBron
      expect(pl.heightInches).toBeGreaterThan(60);
      expect(pl.heightInches).toBeLessThan(92);
    }
  });
});
