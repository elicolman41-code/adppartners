import type {
  CategoryParams,
  Evidence,
  Player,
  SpunCategory,
  ValidationResult,
  ValidatorKey,
} from '../types';
import {
  ageAsOfReference,
  decadesPlayed,
  latestTeamId,
  playedForTeam,
  playedForTeamInDecade,
} from '../data/db';
import { teamName } from '../data/teams';

// Deterministic eligibility checks. Every ruling returns evidence rows so
// disputes can be settled from structured data, never from AI guessing.

interface Ruling {
  eligible: boolean;
  reason: string;
  evidence: Evidence[];
}

type ValidatorFn = (player: Player, params: CategoryParams) => Ruling;

function ev(player: Player, field: string, expected: string, actual: string): Evidence {
  return { field, expected, actual, sourceNote: player.sourceNote };
}

function feetInches(total: number): string {
  return `${Math.floor(total / 12)}′${total % 12}″`;
}

function countRuling(
  player: Player,
  field: string,
  count: number,
  needed: string,
  eligible: boolean,
  yes: string,
  no: string,
): Ruling {
  return {
    eligible,
    reason: eligible ? yes : no,
    evidence: [ev(player, field, needed, String(count))],
  };
}

export const VALIDATORS: Record<ValidatorKey, ValidatorFn> = {
  has_mvp: (pl) =>
    countRuling(pl, 'MVP awards', pl.awards.mvp, '1 or more', pl.awards.mvp > 0,
      `${pl.displayName} won the MVP award ${pl.awards.mvp} time${pl.awards.mvp === 1 ? '' : 's'}.`,
      `${pl.displayName} never won an MVP award.`),

  has_finals_mvp: (pl) =>
    countRuling(pl, 'Finals MVP awards', pl.awards.finalsMvp, '1 or more', pl.awards.finalsMvp > 0,
      `${pl.displayName} won Finals MVP ${pl.awards.finalsMvp} time${pl.awards.finalsMvp === 1 ? '' : 's'}.`,
      `${pl.displayName} never won a Finals MVP.`),

  has_dpoy: (pl) =>
    countRuling(pl, 'DPOY awards', pl.awards.dpoy, '1 or more', pl.awards.dpoy > 0,
      `${pl.displayName} won Defensive Player of the Year ${pl.awards.dpoy} time${pl.awards.dpoy === 1 ? '' : 's'}.`,
      `${pl.displayName} never won Defensive Player of the Year.`),

  has_roty: (pl) =>
    countRuling(pl, 'Rookie of the Year', pl.awards.roty ? 1 : 0, '1', pl.awards.roty,
      `${pl.displayName} won Rookie of the Year.`,
      `${pl.displayName} did not win Rookie of the Year.`),

  has_sixth_man: (pl) =>
    countRuling(pl, 'Sixth Man awards', pl.awards.sixthMan, '1 or more', pl.awards.sixthMan > 0,
      `${pl.displayName} won Sixth Man of the Year ${pl.awards.sixthMan} time${pl.awards.sixthMan === 1 ? '' : 's'}.`,
      `${pl.displayName} never won Sixth Man of the Year.`),

  latest_all_nba: (pl) =>
    countRuling(pl, '2024-25 All-NBA', pl.awards.latestAllNba ? 1 : 0, 'selected', pl.awards.latestAllNba,
      `${pl.displayName} made the 2024-25 All-NBA team.`,
      `${pl.displayName} did not make the 2024-25 All-NBA team.`),

  any_all_nba: (pl) =>
    countRuling(pl, 'All-NBA selections', pl.awards.allNba, '1 or more', pl.awards.allNba > 0,
      `${pl.displayName} made All-NBA ${pl.awards.allNba} time${pl.awards.allNba === 1 ? '' : 's'}.`,
      `${pl.displayName} never made an All-NBA team.`),

  any_all_defense: (pl) =>
    countRuling(pl, 'All-Defensive selections', pl.awards.allDefense, '1 or more', pl.awards.allDefense > 0,
      `${pl.displayName} made All-Defense ${pl.awards.allDefense} time${pl.awards.allDefense === 1 ? '' : 's'}.`,
      `${pl.displayName} never made an All-Defensive team.`),

  any_all_star: (pl) =>
    countRuling(pl, 'All-Star selections', pl.awards.allStar, '1 or more', pl.awards.allStar > 0,
      `${pl.displayName} is a ${pl.awards.allStar}x All-Star.`,
      `${pl.displayName} never made an All-Star team.`),

  never_all_star: (pl) =>
    countRuling(pl, 'All-Star selections', pl.awards.allStar, '0', pl.awards.allStar === 0,
      `${pl.displayName} never made an All-Star team.`,
      `${pl.displayName} made ${pl.awards.allStar} All-Star team${pl.awards.allStar === 1 ? '' : 's'} — too many for this category.`),

  exactly_one_all_star: (pl) =>
    countRuling(pl, 'All-Star selections', pl.awards.allStar, 'exactly 1', pl.awards.allStar === 1,
      `${pl.displayName} made exactly one All-Star team.`,
      pl.awards.allStar === 0
        ? `${pl.displayName} never made an All-Star team — needs exactly one.`
        : `${pl.displayName} made ${pl.awards.allStar} All-Star teams — needs exactly one.`),

  ten_plus_all_star: (pl) =>
    countRuling(pl, 'All-Star selections', pl.awards.allStar, '10 or more', pl.awards.allStar >= 10,
      `${pl.displayName} is a ${pl.awards.allStar}x All-Star.`,
      `${pl.displayName} made ${pl.awards.allStar} All-Star team${pl.awards.allStar === 1 ? '' : 's'} — fewer than 10.`),

  led_scoring: (pl) =>
    countRuling(pl, 'Scoring titles', pl.awards.scoringTitles, '1 or more', pl.awards.scoringTitles > 0,
      `${pl.displayName} led the league in scoring ${pl.awards.scoringTitles} time${pl.awards.scoringTitles === 1 ? '' : 's'}.`,
      `${pl.displayName} never led the league in scoring.`),

  led_assists: (pl) =>
    countRuling(pl, 'Assist titles', pl.awards.assistTitles, '1 or more', pl.awards.assistTitles > 0,
      `${pl.displayName} led the league in assists ${pl.awards.assistTitles} time${pl.awards.assistTitles === 1 ? '' : 's'}.`,
      `${pl.displayName} never led the league in assists.`),

  led_rebounds: (pl) =>
    countRuling(pl, 'Rebounding titles', pl.awards.reboundTitles, '1 or more', pl.awards.reboundTitles > 0,
      `${pl.displayName} led the league in rebounding ${pl.awards.reboundTitles} time${pl.awards.reboundTitles === 1 ? '' : 's'}.`,
      `${pl.displayName} never led the league in rebounding.`),

  led_steals: (pl) =>
    countRuling(pl, 'Steals titles', pl.awards.stealsTitles, '1 or more', pl.awards.stealsTitles > 0,
      `${pl.displayName} led the league in steals ${pl.awards.stealsTitles} time${pl.awards.stealsTitles === 1 ? '' : 's'}.`,
      `${pl.displayName} never led the league in steals.`),

  led_blocks: (pl) =>
    countRuling(pl, 'Blocks titles', pl.awards.blocksTitles, '1 or more', pl.awards.blocksTitles > 0,
      `${pl.displayName} led the league in blocks ${pl.awards.blocksTitles} time${pl.awards.blocksTitles === 1 ? '' : 's'}.`,
      `${pl.displayName} never led the league in blocks.`),

  never_won_ring: (pl) =>
    countRuling(pl, 'Championships', pl.championships, '0', pl.championships === 0,
      `${pl.displayName} never won a championship.`,
      `${pl.displayName} won ${pl.championships} championship${pl.championships === 1 ? '' : 's'} — that disqualifies the pick.`),

  won_ring: (pl) =>
    countRuling(pl, 'Championships', pl.championships, '1 or more', pl.championships > 0,
      `${pl.displayName} won ${pl.championships} championship${pl.championships === 1 ? '' : 's'}.`,
      `${pl.displayName} never won a championship.`),

  active_under_25: (pl) => {
    const age = ageAsOfReference(pl);
    if (!pl.active) {
      return {
        eligible: false,
        reason: `${pl.displayName} is not an active NBA player.`,
        evidence: [ev(pl, 'Active status', 'active in 2025-26', 'not active')],
      };
    }
    return {
      eligible: age < 25,
      reason:
        age < 25
          ? `${pl.displayName} is an active player, age ${age}.`
          : `${pl.displayName} is active but is ${age} — not under 25.`,
      evidence: [
        ev(pl, 'Active status', 'active in 2025-26', 'active'),
        ev(pl, 'Age', 'under 25', `${age} (born ${pl.birthYear})`),
      ],
    };
  },

  under_6_3: (pl) => ({
    eligible: pl.heightInches < 75,
    reason:
      pl.heightInches < 75
        ? `${pl.displayName} is listed at ${feetInches(pl.heightInches)} — under 6′3″.`
        : `${pl.displayName} is listed at ${feetInches(pl.heightInches)}, which is not under the 6′3″ limit.`,
    evidence: [ev(pl, 'Listed height', 'under 6′3″ (75 in)', `${feetInches(pl.heightInches)} (${pl.heightInches} in)`)],
  }),

  seven_foot_plus: (pl) => ({
    eligible: pl.heightInches >= 84,
    reason:
      pl.heightInches >= 84
        ? `${pl.displayName} is listed at ${feetInches(pl.heightInches)} — 7 feet or taller.`
        : `${pl.displayName} is listed at ${feetInches(pl.heightInches)}, shorter than 7′0″.`,
    evidence: [ev(pl, 'Listed height', '7′0″ or taller (84 in)', `${feetInches(pl.heightInches)} (${pl.heightInches} in)`)],
  }),

  international: (pl) => ({
    eligible: pl.birthCountry !== 'USA',
    reason:
      pl.birthCountry !== 'USA'
        ? `${pl.displayName} was born in ${pl.birthCountry}.`
        : `${pl.displayName} was born in the USA.`,
    evidence: [ev(pl, 'Birth country', 'not USA', pl.birthCountry)],
  }),

  top_3_pick: (pl) => {
    const pick = pl.draftPick;
    const eligible = pick !== null && pick <= 3;
    return {
      eligible,
      reason: eligible
        ? `${pl.displayName} was the No. ${pick} overall pick in ${pl.draftYear}.`
        : pick === null
          ? `${pl.displayName} has no recorded top-3 pick — ${pl.draftRound === null ? 'went undrafted' : 'no overall pick number on record'}.`
          : `${pl.displayName} was picked No. ${pick} overall in ${pl.draftYear} — outside the top 3.`,
      evidence: [ev(pl, 'Draft pick', '1, 2, or 3', pick === null ? 'none recorded' : `No. ${pick} (${pl.draftYear})`)],
    };
  },

  second_round_pick: (pl) => {
    const eligible = pl.draftRound === 2;
    return {
      eligible,
      reason: eligible
        ? `${pl.displayName} was a second-round pick (No. ${pl.draftPick} overall, ${pl.draftYear}).`
        : pl.draftRound === null
          ? `${pl.displayName} went undrafted — not a second-round pick.`
          : `${pl.displayName} was drafted in round ${pl.draftRound}, not round 2.`,
      evidence: [ev(pl, 'Draft round', '2', pl.draftRound === null ? 'undrafted' : `round ${pl.draftRound}`)],
    };
  },

  undrafted: (pl) => {
    const eligible = pl.draftRound === null;
    return {
      eligible,
      reason: eligible
        ? `${pl.displayName} went undrafted.`
        : `${pl.displayName} was drafted in ${pl.draftYear} (round ${pl.draftRound}${pl.draftPick ? `, pick ${pl.draftPick}` : ''}).`,
      evidence: [ev(pl, 'Draft status', 'undrafted', eligible ? 'undrafted' : `drafted ${pl.draftYear}`)],
    };
  },

  played_in_decade: (pl, params) => {
    const decade = params.decade ?? 0;
    const played = decadesPlayed(pl).includes(decade);
    return {
      eligible: played,
      reason: played
        ? `${pl.displayName} played in the ${decade}s.`
        : `${pl.displayName} did not play an NBA season in the ${decade}s.`,
      evidence: [ev(pl, 'Decades played', `${decade}s`, decadesPlayed(pl).map((d) => `${d}s`).join(', ') || 'none')],
    };
  },

  played_for_team: (pl, params) => {
    const teamId = params.teamId ?? '';
    const played = playedForTeam(pl, teamId);
    return {
      eligible: played,
      reason: played
        ? `${pl.displayName} played for the ${teamName(teamId)} franchise.`
        : `${pl.displayName} never played for the ${teamName(teamId)} franchise.`,
      evidence: [
        ev(pl, 'Franchises', teamName(teamId), [...new Set(pl.seasons.map((s) => teamName(s.teamId)))].join(', ')),
      ],
    };
  },

  played_for_team_in_decade: (pl, params) => {
    const teamId = params.teamId ?? '';
    const decade = params.decade ?? 0;
    const ok = playedForTeamInDecade(pl, teamId, decade);
    return {
      eligible: ok,
      reason: ok
        ? `${pl.displayName} played for the ${teamName(teamId)} in the ${decade}s.`
        : `${pl.displayName} did not play for the ${teamName(teamId)} in the ${decade}s.`,
      evidence: [
        ev(
          pl,
          'Team history',
          `${teamName(teamId)} in the ${decade}s`,
          pl.seasons.map((s) => `${teamName(s.teamId)} ${s.from}-${s.to + 1}`).join('; '),
        ),
      ],
    };
  },
};

/** Run a category ruling against a resolved player. */
export function validatePick(player: Player, category: SpunCategory): ValidationResult {
  const ruling = VALIDATORS[category.validatorKey](player, category.params);
  return {
    eligible: ruling.eligible,
    reason: ruling.reason,
    player: {
      id: player.id,
      displayName: player.displayName,
      positions: player.positions,
      team: latestTeamId(player),
    },
    evidence: ruling.evidence,
  };
}

/** Count of players in the pool that satisfy a category (for the generator). */
export function eligibleCount(players: Player[], key: ValidatorKey, params: CategoryParams): number {
  const fn = VALIDATORS[key];
  let n = 0;
  for (const pl of players) if (fn(pl, params).eligible) n++;
  return n;
}
