import { describe, expect, it } from 'vitest';
import type { SpunCategory, ValidatorKey } from '../types';
import { PLAYERS, PLAYER_BY_ID } from '../data/db';
import { CATEGORIES } from '../data/categories';
import { eligibleCount, validatePick, VALIDATORS } from './validators';

function cat(key: ValidatorKey, params: SpunCategory['params'] = {}): SpunCategory {
  return { definitionId: `test-${key}`, label: key, validatorKey: key, params };
}

function check(playerId: string, key: ValidatorKey, params: SpunCategory['params'] = {}) {
  const player = PLAYER_BY_ID[playerId];
  expect(player, `player ${playerId} must exist in seed data`).toBeTruthy();
  return validatePick(player, cat(key, params));
}

describe('data integrity', () => {
  it('seeds at least 150 players (plan minimum is 100)', () => {
    expect(PLAYERS.length).toBeGreaterThanOrEqual(150);
  });

  it('has no duplicate player ids', () => {
    const ids = PLAYERS.map((p) => p.id);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('defines exactly 30 categories', () => {
    expect(CATEGORIES.length).toBe(30);
  });

  it('every category has a registered validator', () => {
    for (const def of CATEGORIES) {
      expect(VALIDATORS[def.validatorKey], def.id).toBeTypeOf('function');
    }
  });

  it('every player has at least one season stint and a source note', () => {
    for (const pl of PLAYERS) {
      expect(pl.seasons.length, pl.id).toBeGreaterThan(0);
      expect(pl.sourceNote.length, pl.id).toBeGreaterThan(0);
    }
  });

  it('every fixed category is playable (enough eligible players)', () => {
    for (const def of CATEGORIES) {
      if (def.needsParams?.length) continue;
      const n = eligibleCount(PLAYERS, def.validatorKey, def.params ?? {});
      expect(n, `${def.id} needs >= 6 eligible players, has ${n}`).toBeGreaterThanOrEqual(6);
    }
  });
});

describe('award validators', () => {
  it('has_mvp: LeBron eligible, Ewing not', () => {
    expect(check('lebron-james', 'has_mvp').eligible).toBe(true);
    const r = check('patrick-ewing', 'has_mvp');
    expect(r.eligible).toBe(false);
    expect(r.reason).toContain('never won an MVP');
  });

  it('has_finals_mvp: Jerry West (the original) eligible, Karl Malone not', () => {
    expect(check('jerry-west', 'has_finals_mvp').eligible).toBe(true);
    expect(check('karl-malone', 'has_finals_mvp').eligible).toBe(false);
  });

  it('has_dpoy: Ben Wallace eligible, Tim Duncan famously not', () => {
    expect(check('ben-wallace', 'has_dpoy').eligible).toBe(true);
    expect(check('tim-duncan', 'has_dpoy').eligible).toBe(false);
  });

  it('has_roty: Magic did NOT win ROTY (Bird did)', () => {
    expect(check('magic-johnson', 'has_roty').eligible).toBe(false);
    expect(check('larry-bird', 'has_roty').eligible).toBe(true);
  });

  it('has_sixth_man: Lou Williams and Harden eligible, Iguodala not', () => {
    expect(check('lou-williams', 'has_sixth_man').eligible).toBe(true);
    expect(check('james-harden', 'has_sixth_man').eligible).toBe(true);
    expect(check('andre-iguodala', 'has_sixth_man').eligible).toBe(false);
  });

  it('latest_all_nba: 2024-25 team members pass, Luka does not', () => {
    for (const id of ['shai-gilgeous-alexander', 'nikola-jokic', 'jalen-brunson', 'evan-mobley', 'jalen-williams']) {
      expect(check(id, 'latest_all_nba').eligible, id).toBe(true);
    }
    expect(check('luka-doncic', 'latest_all_nba').eligible).toBe(false);
  });

  it('never_all_star vs any_all_star are exact complements across the pool', () => {
    for (const pl of PLAYERS) {
      const never = VALIDATORS.never_all_star(pl, {}).eligible;
      const any = VALIDATORS.any_all_star(pl, {}).eligible;
      expect(never).toBe(!any);
    }
  });

  it('never_all_star: Robert Horry (7 rings) and Jamal Murray eligible', () => {
    expect(check('robert-horry', 'never_all_star').eligible).toBe(true);
    expect(check('jamal-murray', 'never_all_star').eligible).toBe(true);
    expect(check('michael-jordan', 'never_all_star').eligible).toBe(false);
  });

  it('exactly_one_all_star: Fred VanVleet eligible; 0x and 2x both fail', () => {
    expect(check('fred-vanvleet', 'exactly_one_all_star').eligible).toBe(true);
    expect(check('alex-caruso', 'exactly_one_all_star').eligible).toBe(false);
    expect(check('isaiah-thomas', 'exactly_one_all_star').eligible).toBe(false);
  });

  it('ten_plus_all_star: Kobe eligible, Reggie Miller (5x) not', () => {
    expect(check('kobe-bryant', 'ten_plus_all_star').eligible).toBe(true);
    expect(check('reggie-miller', 'ten_plus_all_star').eligible).toBe(false);
  });
});

describe('league-leader validators', () => {
  it('led_scoring: Jordan yes, Karl Malone famously never', () => {
    expect(check('michael-jordan', 'led_scoring').eligible).toBe(true);
    expect(check('karl-malone', 'led_scoring').eligible).toBe(false);
  });

  it('led_assists: Stockton yes, Jokić no', () => {
    expect(check('john-stockton', 'led_assists').eligible).toBe(true);
    expect(check('nikola-jokic', 'led_assists').eligible).toBe(false);
  });

  it('led_rebounds: Rodman yes, Shaq famously never', () => {
    expect(check('dennis-rodman', 'led_rebounds').eligible).toBe(true);
    expect(check('shaquille-oneal', 'led_rebounds').eligible).toBe(false);
  });

  it('led_steals: Chris Paul yes, Muggsy no', () => {
    expect(check('chris-paul', 'led_steals').eligible).toBe(true);
    expect(check('muggsy-bogues', 'led_steals').eligible).toBe(false);
  });

  it('led_blocks: Mark Eaton yes, Kevin Garnett no', () => {
    expect(check('mark-eaton', 'led_blocks').eligible).toBe(true);
    expect(check('kevin-garnett', 'led_blocks').eligible).toBe(false);
  });
});

describe('ring validators', () => {
  it('never_won_ring: Barkley/Ewing/Nash eligible, Horry very much not', () => {
    expect(check('charles-barkley', 'never_won_ring').eligible).toBe(true);
    expect(check('patrick-ewing', 'never_won_ring').eligible).toBe(true);
    expect(check('steve-nash', 'never_won_ring').eligible).toBe(true);
    const horry = check('robert-horry', 'never_won_ring');
    expect(horry.eligible).toBe(false);
    expect(horry.reason).toContain('7');
  });

  it('won_ring: Alex Caruso (2 rings) eligible, Chris Paul not', () => {
    expect(check('alex-caruso', 'won_ring').eligible).toBe(true);
    expect(check('chris-paul', 'won_ring').eligible).toBe(false);
  });
});

describe('bio validators', () => {
  it('active_under_25: Wemby eligible; retired player fails on active status', () => {
    expect(check('victor-wembanyama', 'active_under_25').eligible).toBe(true);
    const jordan = check('michael-jordan', 'active_under_25');
    expect(jordan.eligible).toBe(false);
    expect(jordan.reason).toContain('not an active');
    const lebron = check('lebron-james', 'active_under_25');
    expect(lebron.eligible).toBe(false); // active but 41
  });

  it('under_6_3: the Kevin Durant example from the plan rules him out', () => {
    const kd = check('kevin-durant', 'under_6_3');
    expect(kd.eligible).toBe(false);
    expect(kd.evidence[0].field).toBe('Listed height');
    expect(check('muggsy-bogues', 'under_6_3').eligible).toBe(true);
    expect(check('isaiah-thomas', 'under_6_3').eligible).toBe(true);
  });

  it('under_6_3 boundary: exactly 6-3 (75in) is NOT eligible', () => {
    const mitchell = PLAYER_BY_ID['donovan-mitchell'];
    expect(mitchell.heightInches).toBe(75);
    expect(check('donovan-mitchell', 'under_6_3').eligible).toBe(false);
  });

  it('seven_foot_plus boundary: exactly 7-0 (84in) IS eligible', () => {
    expect(PLAYER_BY_ID['patrick-ewing'].heightInches).toBe(84);
    expect(check('patrick-ewing', 'seven_foot_plus').eligible).toBe(true);
    expect(check('kevin-durant', 'seven_foot_plus').eligible).toBe(false); // 6'10"
  });

  it('international: Giannis, Kyrie (born Australia), Parker (born Belgium) eligible; KAT not', () => {
    expect(check('giannis-antetokounmpo', 'international').eligible).toBe(true);
    expect(check('kyrie-irving', 'international').eligible).toBe(true);
    expect(check('tony-parker', 'international').eligible).toBe(true);
    expect(check('karl-anthony-towns', 'international').eligible).toBe(false);
  });

  it('top_3_pick: Jordan (No. 3) eligible; Kobe (13) and undrafted fail', () => {
    expect(check('michael-jordan', 'top_3_pick').eligible).toBe(true);
    expect(check('kobe-bryant', 'top_3_pick').eligible).toBe(false);
    expect(check('ben-wallace', 'top_3_pick').eligible).toBe(false);
  });

  it('second_round_pick: Jokić (41st) and Draymond (35th) eligible; Manu (57th) too', () => {
    expect(check('nikola-jokic', 'second_round_pick').eligible).toBe(true);
    expect(check('draymond-green', 'second_round_pick').eligible).toBe(true);
    expect(check('manu-ginobili', 'second_round_pick').eligible).toBe(true);
    expect(check('michael-jordan', 'second_round_pick').eligible).toBe(false);
    expect(check('ben-wallace', 'second_round_pick').eligible).toBe(false); // undrafted != round 2
  });

  it('undrafted: Ben Wallace/FVV/Caruso eligible; 60th pick IT is not', () => {
    expect(check('ben-wallace', 'undrafted').eligible).toBe(true);
    expect(check('fred-vanvleet', 'undrafted').eligible).toBe(true);
    expect(check('alex-caruso', 'undrafted').eligible).toBe(true);
    expect(check('isaiah-thomas', 'undrafted').eligible).toBe(false);
  });
});

describe('history validators', () => {
  it('played_in_decade: Jordan played in both the 80s and 90s; LeBron in neither', () => {
    expect(check('michael-jordan', 'played_in_decade', { decade: 1980 }).eligible).toBe(true);
    expect(check('michael-jordan', 'played_in_decade', { decade: 1990 }).eligible).toBe(true);
    expect(check('lebron-james', 'played_in_decade', { decade: 1990 }).eligible).toBe(false);
    expect(check('lebron-james', 'played_in_decade', { decade: 2000 }).eligible).toBe(true);
  });

  it('played_for_team: franchise mapping counts Seattle as OKC and NJ as Brooklyn', () => {
    expect(check('gary-payton', 'played_for_team', { teamId: 'OKC' }).eligible).toBe(true);
    expect(check('jason-kidd', 'played_for_team', { teamId: 'BKN' }).eligible).toBe(true);
    expect(check('tim-duncan', 'played_for_team', { teamId: 'LAL' }).eligible).toBe(false);
  });

  it('played_for_team_in_decade: KD played for OKC in the 2010s but not the 2020s', () => {
    expect(check('kevin-durant', 'played_for_team_in_decade', { teamId: 'OKC', decade: 2010 }).eligible).toBe(true);
    expect(check('kevin-durant', 'played_for_team_in_decade', { teamId: 'OKC', decade: 2020 }).eligible).toBe(false);
    expect(check('kobe-bryant', 'played_for_team_in_decade', { teamId: 'LAL', decade: 1990 }).eligible).toBe(true);
    expect(check('kobe-bryant', 'played_for_team_in_decade', { teamId: 'LAL', decade: 2020 }).eligible).toBe(false);
  });
});

describe('validation response shape (from the build plan)', () => {
  it('returns eligible, reason, player, and evidence fields', () => {
    const r = check('kevin-durant', 'under_6_3');
    expect(r).toMatchObject({
      eligible: false,
      player: { id: 'kevin-durant', displayName: 'Kevin Durant', positions: ['SF', 'PF'] },
    });
    expect(r.reason.length).toBeGreaterThan(10);
    expect(r.evidence.length).toBeGreaterThan(0);
    expect(r.evidence[0]).toHaveProperty('field');
    expect(r.evidence[0]).toHaveProperty('expected');
    expect(r.evidence[0]).toHaveProperty('actual');
    expect(r.evidence[0]).toHaveProperty('sourceNote');
  });
});
