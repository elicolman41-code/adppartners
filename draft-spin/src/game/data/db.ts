import type { Player } from '../types';
import { PLAYERS_LEGENDS } from './playersLegends';
import { PLAYERS_2000S } from './players2000s';
import { PLAYERS_2010S } from './players2010s';
import { PLAYERS_MODERN } from './playersModern';

export const PLAYERS: Player[] = [
  ...PLAYERS_LEGENDS,
  ...PLAYERS_2000S,
  ...PLAYERS_2010S,
  ...PLAYERS_MODERN,
];

export const PLAYER_BY_ID: Record<string, Player> = Object.fromEntries(
  PLAYERS.map((pl) => [pl.id, pl]),
);

/** Latest team a player suited up for (by stint end year). */
export function latestTeamId(player: Player): string {
  let best = player.seasons[0];
  for (const s of player.seasons) {
    if (s.to > best.to) best = s;
  }
  return best?.teamId ?? '';
}

/** Every decade (as start year, e.g. 1990) the player logged a season in. */
export function decadesPlayed(player: Player): number[] {
  const decades = new Set<number>();
  for (const s of player.seasons) {
    for (let y = s.from; y <= s.to; y++) {
      decades.add(Math.floor(y / 10) * 10);
    }
  }
  return [...decades].sort();
}

export function playedForTeam(player: Player, teamId: string): boolean {
  return player.seasons.some((s) => s.teamId === teamId);
}

export function playedForTeamInDecade(player: Player, teamId: string, decade: number): boolean {
  return player.seasons.some(
    (s) => s.teamId === teamId && s.from <= decade + 9 && s.to >= decade,
  );
}

/** Age during the current (2025-26) season, computed from birth year. */
export const AGE_REFERENCE_YEAR = 2026;

export function ageAsOfReference(player: Player): number {
  return AGE_REFERENCE_YEAR - player.birthYear;
}
