import type { CategoryDefinition } from '../types';

// The 30 launch categories from the build plan, in order.
export const CATEGORIES: CategoryDefinition[] = [
  { id: 'cat-mvp', label: 'Won an MVP award', validatorKey: 'has_mvp', difficulty: 1 },
  { id: 'cat-finals-mvp', label: 'Won a Finals MVP', validatorKey: 'has_finals_mvp', difficulty: 1 },
  { id: 'cat-dpoy', label: 'Won Defensive Player of the Year', validatorKey: 'has_dpoy', difficulty: 2 },
  { id: 'cat-roty', label: 'Won Rookie of the Year', validatorKey: 'has_roty', difficulty: 1 },
  { id: 'cat-sixth-man', label: 'Won Sixth Man of the Year', validatorKey: 'has_sixth_man', difficulty: 3 },
  { id: 'cat-current-all-nba', label: 'Made the latest All-NBA team (2024-25)', validatorKey: 'latest_all_nba', difficulty: 2 },
  { id: 'cat-any-all-nba', label: 'Made any All-NBA team', validatorKey: 'any_all_nba', difficulty: 1 },
  { id: 'cat-all-defense', label: 'Made an All-Defensive team', validatorKey: 'any_all_defense', difficulty: 2 },
  { id: 'cat-all-star', label: 'Made an All-Star team', validatorKey: 'any_all_star', difficulty: 1 },
  { id: 'cat-never-all-star', label: 'NEVER made an All-Star team', validatorKey: 'never_all_star', difficulty: 3 },
  { id: 'cat-one-all-star', label: 'Made EXACTLY one All-Star team', validatorKey: 'exactly_one_all_star', difficulty: 3 },
  { id: 'cat-ten-all-star', label: 'Made 10+ All-Star teams', validatorKey: 'ten_plus_all_star', difficulty: 2 },
  { id: 'cat-led-scoring', label: 'Led the league in scoring', validatorKey: 'led_scoring', difficulty: 2 },
  { id: 'cat-led-assists', label: 'Led the league in assists', validatorKey: 'led_assists', difficulty: 2 },
  { id: 'cat-led-rebounds', label: 'Led the league in rebounds', validatorKey: 'led_rebounds', difficulty: 2 },
  { id: 'cat-led-steals', label: 'Led the league in steals', validatorKey: 'led_steals', difficulty: 3 },
  { id: 'cat-led-blocks', label: 'Led the league in blocks', validatorKey: 'led_blocks', difficulty: 3 },
  { id: 'cat-no-ring', label: 'NEVER won a championship', validatorKey: 'never_won_ring', difficulty: 1 },
  { id: 'cat-ring', label: 'Won a championship', validatorKey: 'won_ring', difficulty: 1 },
  { id: 'cat-under-25', label: 'Current player under age 25', validatorKey: 'active_under_25', difficulty: 2 },
  { id: 'cat-under-6-3', label: 'Listed under 6′3″', validatorKey: 'under_6_3', difficulty: 2 },
  { id: 'cat-seven-foot', label: 'Listed 7′0″ or taller', validatorKey: 'seven_foot_plus', difficulty: 2 },
  { id: 'cat-international', label: 'Born outside the USA', validatorKey: 'international', difficulty: 1 },
  { id: 'cat-top-3-pick', label: 'Top-3 draft pick', validatorKey: 'top_3_pick', difficulty: 1 },
  { id: 'cat-second-round', label: 'Drafted in the second round', validatorKey: 'second_round_pick', difficulty: 3 },
  { id: 'cat-undrafted', label: 'Went undrafted', validatorKey: 'undrafted', difficulty: 3 },
  { id: 'cat-played-1980s', label: 'Played in the 1980s', validatorKey: 'played_in_decade', difficulty: 2, params: { decade: 1980 } },
  { id: 'cat-played-1990s', label: 'Played in the 1990s', validatorKey: 'played_in_decade', difficulty: 2, params: { decade: 1990 } },
  { id: 'cat-played-for-team', label: 'Played for the {team}', validatorKey: 'played_for_team', difficulty: 2, needsParams: ['team'] },
  { id: 'cat-team-decade', label: 'Played for the {team} in the {decade}s', validatorKey: 'played_for_team_in_decade', difficulty: 3, needsParams: ['team', 'decade'] },
];

export const CATEGORY_BY_ID: Record<string, CategoryDefinition> = Object.fromEntries(
  CATEGORIES.map((c) => [c.id, c]),
);
