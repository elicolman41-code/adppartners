// Draft Spin core types — mirrors the table shape from the build plan:
// players, player_aliases, teams, player_team_seasons, player_awards,
// championships, category_definitions, matches/rounds/picks, series_results.

export type Position = 'PG' | 'SG' | 'SF' | 'PF' | 'C';

export const POSITION_ORDER: Position[] = ['PG', 'SG', 'SF', 'PF', 'C'];

export const POSITION_NAMES: Record<Position, string> = {
  PG: 'Point Guard',
  SG: 'Shooting Guard',
  SF: 'Small Forward',
  PF: 'Power Forward',
  C: 'Center',
};

export interface Team {
  id: string; // canonical franchise abbreviation, e.g. 'LAL'
  name: string; // current franchise name
  /** Historical names covered by this franchise id (for display + audit). */
  historicalNames?: string[];
}

export interface PlayerAwards {
  mvp: number;
  finalsMvp: number;
  dpoy: number;
  roty: boolean;
  sixthMan: number;
  allNba: number;
  /** Made the latest completed All-NBA team (2024-25). */
  latestAllNba: boolean;
  allDefense: number;
  allStar: number;
  scoringTitles: number;
  assistTitles: number;
  reboundTitles: number;
  stealsTitles: number;
  blocksTitles: number;
}

/** Simulator ratings, 0-100. */
export interface PlayerRatings {
  scoring: number;
  creation: number;
  shooting: number;
  perimeterDefense: number;
  rimProtection: number;
  rebounding: number;
}

export interface TeamStint {
  teamId: string;
  /** Season start years, inclusive: 1996 means the 1996-97 season. */
  from: number;
  to: number;
}

export interface Player {
  id: string;
  displayName: string;
  /** Every position the player can credibly play, primary first. */
  positions: Position[];
  heightInches: number;
  birthCountry: string;
  birthYear: number;
  active: boolean; // active as of the 2025-26 season
  draftYear: number | null;
  draftRound: number | null; // null = undrafted
  draftPick: number | null; // overall pick number
  aliases: string[];
  awards: PlayerAwards;
  championships: number; // rings won as a player
  seasons: TeamStint[];
  /** 1 = all-time great … 5 = role player. Drives simulator talent. */
  tier: 1 | 2 | 3 | 4 | 5;
  ratings: PlayerRatings;
  /** 0-100, how much the player needs the ball. Drives fit penalties. */
  ballDominance: number;
  sourceNote: string;
}

// ---------------------------------------------------------------------------
// Categories
// ---------------------------------------------------------------------------

export type ValidatorKey =
  | 'has_mvp'
  | 'has_finals_mvp'
  | 'has_dpoy'
  | 'has_roty'
  | 'has_sixth_man'
  | 'latest_all_nba'
  | 'any_all_nba'
  | 'any_all_defense'
  | 'any_all_star'
  | 'never_all_star'
  | 'exactly_one_all_star'
  | 'ten_plus_all_star'
  | 'led_scoring'
  | 'led_assists'
  | 'led_rebounds'
  | 'led_steals'
  | 'led_blocks'
  | 'never_won_ring'
  | 'won_ring'
  | 'active_under_25'
  | 'under_6_3'
  | 'seven_foot_plus'
  | 'international'
  | 'top_3_pick'
  | 'second_round_pick'
  | 'undrafted'
  | 'played_in_decade'
  | 'played_for_team'
  | 'played_for_team_in_decade';

export interface CategoryParams {
  teamId?: string;
  decade?: number; // 1980 means the 1980s
}

export interface CategoryDefinition {
  id: string;
  label: string; // may contain {team} / {decade} placeholders
  validatorKey: ValidatorKey;
  /** 1 easy … 3 hard. Used to balance rounds. */
  difficulty: 1 | 2 | 3;
  params?: CategoryParams;
  /** Requires runtime param generation (random team / decade). */
  needsParams?: ('team' | 'decade')[];
}

/** A category instance actually shown in a round (params resolved). */
export interface SpunCategory {
  definitionId: string;
  label: string;
  validatorKey: ValidatorKey;
  params: CategoryParams;
}

// ---------------------------------------------------------------------------
// Validation — response shape straight from the build plan
// ---------------------------------------------------------------------------

export interface Evidence {
  field: string;
  expected: string;
  actual: string;
  sourceNote: string;
}

export interface ValidationResult {
  eligible: boolean;
  reason: string;
  player: {
    id: string;
    displayName: string;
    positions: Position[];
    team: string; // most recent team id
  };
  evidence: Evidence[];
}

// ---------------------------------------------------------------------------
// Match state
// ---------------------------------------------------------------------------

export type PickOutcome = 'eligible' | 'ineligible' | 'duplicate';

/**
 * A ruled attempt. No point math: an eligible pick locks the player into the
 * roster and ends that side's turn for the round; an ineligible or duplicate
 * pick is crossed out (X) and the turn passes to the other player on the same
 * category — nobody loses a roster spot, both sides always finish with five.
 */
export interface Pick {
  playerId: string;
  outcome: PickOutcome;
  reason: string;
  evidence: Evidence[];
}

export interface Round {
  index: number; // 0-based
  category: SpunCategory;
  /** Every ruled attempt in order. A side is done once it has an eligible one. */
  attempts: { participantId: string; pick: Pick }[];
}

export interface Participant {
  id: string;
  name: string;
  roster: string[]; // eligible player ids, locked in
  /** Set when this seat is played by the computer. */
  ai?: 'rookie' | 'veteran' | 'goat';
}

export type MatchPhase = 'lobby' | 'spin' | 'pick' | 'reveal' | 'results';

export interface Match {
  id: string;
  roomCode: string;
  createdAt: number;
  totalRounds: number;
  participants: [Participant, Participant];
  rounds: Round[];
  currentRound: number;
  /** whose turn within the round (index into participants) */
  turn: 0 | 1;
  phase: MatchPhase;
  usedCategoryIds: string[];
  /** 1-based game number within a run-it-back chain. */
  game: number;
  /** Players drafted in earlier games of this run — out of the pool for both sides. */
  excludedIds: string[];
  /** Series wins by each side in earlier games of this run. */
  runWins: [number, number];
}

// ---------------------------------------------------------------------------
// Series simulation
// ---------------------------------------------------------------------------

export interface TeamRatingBreakdown {
  talent: number;
  creation: number;
  spacing: number;
  perimeterDefense: number;
  rimProtection: number;
  rebounding: number;
  fitPenalty: number;
  fitNotes: string[];
  overall: number;
}

export interface SimGame {
  index: number; // game 1..7
  homeSide: 0 | 1;
  scores: [number, number];
  winnerSide: 0 | 1;
  closingNote: string;
}

export interface SeriesResult {
  winnerSide: 0 | 1;
  wins: [number, number];
  games: SimGame[];
  mvpPlayerId: string;
  ratings: [TeamRatingBreakdown, TeamRatingBreakdown];
  whyRundown: string[];
}
