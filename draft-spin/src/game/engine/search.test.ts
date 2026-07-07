import { describe, expect, it } from 'vitest';
import { normalizeName, resolvePlayer, searchPlayers } from './search';

describe('normalizeName', () => {
  it('lowercases, strips accents, punctuation, and extra spacing', () => {
    expect(normalizeName('  Nikola   Jokić ')).toBe('nikola jokic');
    expect(normalizeName("Shaquille O'Neal")).toBe('shaquille oneal');
    expect(normalizeName('De’Aaron Fox')).toBe('deaaron fox');
    expect(normalizeName('T-Mac')).toBe('tmac');
  });
});

describe('alias resolution (the exact aliases named in the plan)', () => {
  it.each([
    ['KD', 'Kevin Durant'],
    ['Bron', 'LeBron James'],
    ['AI', 'Allen Iverson'],
    ['T-Mac', 'Tracy McGrady'],
    ['Shaq', 'Shaquille O’Neal'],
    ['Steph', 'Stephen Curry'],
  ])('resolves %s to %s', (alias, expected) => {
    expect(resolvePlayer(alias)?.displayName).toBe(expected);
  });

  it('resolves full names case-insensitively with accents dropped', () => {
    expect(resolvePlayer('nikola jokic')?.id).toBe('nikola-jokic');
    expect(resolvePlayer('LUKA DONCIC')?.id).toBe('luka-doncic');
  });

  it('returns null for typos and unknown players (no penalty path)', () => {
    expect(resolvePlayer('Kevon Duran')).toBeNull();
    expect(resolvePlayer('zzzz')).toBeNull();
  });
});

describe('searchPlayers autocomplete', () => {
  it('returns at most 8 suggestions', () => {
    expect(searchPlayers('a').length).toBeLessThanOrEqual(8);
    expect(searchPlayers('j').length).toBeLessThanOrEqual(8);
  });

  it('puts an exact match first', () => {
    expect(searchPlayers('kd')[0].player.displayName).toBe('Kevin Durant');
    expect(searchPlayers('magic')[0].player.displayName).toBe('Magic Johnson');
  });

  it('matches by last name', () => {
    const hits = searchPlayers('duncan');
    expect(hits.some((h) => h.player.id === 'tim-duncan')).toBe(true);
  });

  it('never returns duplicate players even when name and alias both match', () => {
    const hits = searchPlayers('james');
    const ids = hits.map((h) => h.player.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('returns nothing for empty input', () => {
    expect(searchPlayers('')).toEqual([]);
    expect(searchPlayers('   ')).toEqual([]);
  });
});
