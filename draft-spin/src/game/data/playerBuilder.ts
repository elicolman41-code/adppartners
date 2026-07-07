import type { Player, PlayerAwards, Position } from '../types';

const DEFAULT_NOTE = 'Curated seed data (public career records), July 2026';

export interface AwardsInput {
  mvp?: number;
  fmvp?: number;
  dpoy?: number;
  roty?: 1 | 0;
  smoy?: number;
  allNba?: number;
  latestAllNba?: 1 | 0;
  allDef?: number;
  allStar?: number;
  sco?: number;
  ast?: number;
  reb?: number;
  stl?: number;
  blk?: number;
}

export function a(input: AwardsInput = {}): PlayerAwards {
  return {
    mvp: input.mvp ?? 0,
    finalsMvp: input.fmvp ?? 0,
    dpoy: input.dpoy ?? 0,
    roty: input.roty === 1,
    sixthMan: input.smoy ?? 0,
    allNba: input.allNba ?? 0,
    latestAllNba: input.latestAllNba === 1,
    allDefense: input.allDef ?? 0,
    allStar: input.allStar ?? 0,
    scoringTitles: input.sco ?? 0,
    assistTitles: input.ast ?? 0,
    reboundTitles: input.reb ?? 0,
    stealsTitles: input.stl ?? 0,
    blocksTitles: input.blk ?? 0,
  };
}

export function p(
  id: string,
  displayName: string,
  position: Position,
  heightInches: number,
  birthCountry: string,
  birthYear: number,
  active: 0 | 1,
  draft: [number, number, number] | null,
  aliases: string[],
  awards: PlayerAwards,
  championships: number,
  seasons: [string, number, number][],
  tier: 1 | 2 | 3 | 4 | 5,
  ratings: [number, number, number, number, number, number],
  ballDominance: number,
  sourceNote?: string,
): Player {
  return {
    id,
    displayName,
    position,
    heightInches,
    birthCountry,
    birthYear,
    active: active === 1,
    draftYear: draft ? draft[0] : null,
    draftRound: draft ? draft[1] : null,
    draftPick: draft && draft[2] > 0 ? draft[2] : null,
    aliases,
    awards,
    championships,
    seasons: seasons.map(([teamId, from, to]) => ({ teamId, from, to })),
    tier,
    ratings: {
      scoring: ratings[0],
      creation: ratings[1],
      shooting: ratings[2],
      perimeterDefense: ratings[3],
      rimProtection: ratings[4],
      rebounding: ratings[5],
    },
    ballDominance,
    sourceNote: sourceNote ?? DEFAULT_NOTE,
  };
}
