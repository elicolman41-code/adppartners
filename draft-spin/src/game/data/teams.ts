import type { Team } from '../types';

// Canonical franchise ids. Historical stints (Seattle, New Jersey, the
// Bullets, the New Orleans Hornets years) are recorded under the current
// franchise id so "played for random team" rulings follow franchise history.
export const TEAMS: Team[] = [
  { id: 'ATL', name: 'Atlanta Hawks' },
  { id: 'BOS', name: 'Boston Celtics' },
  { id: 'BKN', name: 'Brooklyn Nets', historicalNames: ['New Jersey Nets'] },
  { id: 'CHA', name: 'Charlotte Hornets', historicalNames: ['Charlotte Bobcats'] },
  { id: 'CHI', name: 'Chicago Bulls' },
  { id: 'CLE', name: 'Cleveland Cavaliers' },
  { id: 'DAL', name: 'Dallas Mavericks' },
  { id: 'DEN', name: 'Denver Nuggets' },
  { id: 'DET', name: 'Detroit Pistons' },
  { id: 'GSW', name: 'Golden State Warriors' },
  { id: 'HOU', name: 'Houston Rockets' },
  { id: 'IND', name: 'Indiana Pacers' },
  { id: 'LAC', name: 'LA Clippers', historicalNames: ['San Diego Clippers'] },
  { id: 'LAL', name: 'Los Angeles Lakers' },
  { id: 'MEM', name: 'Memphis Grizzlies', historicalNames: ['Vancouver Grizzlies'] },
  { id: 'MIA', name: 'Miami Heat' },
  { id: 'MIL', name: 'Milwaukee Bucks' },
  { id: 'MIN', name: 'Minnesota Timberwolves' },
  { id: 'NOP', name: 'New Orleans Pelicans', historicalNames: ['New Orleans Hornets'] },
  { id: 'NYK', name: 'New York Knicks' },
  { id: 'OKC', name: 'Oklahoma City Thunder', historicalNames: ['Seattle SuperSonics'] },
  { id: 'ORL', name: 'Orlando Magic' },
  { id: 'PHI', name: 'Philadelphia 76ers' },
  { id: 'PHX', name: 'Phoenix Suns' },
  { id: 'POR', name: 'Portland Trail Blazers' },
  { id: 'SAC', name: 'Sacramento Kings', historicalNames: ['Kansas City Kings', 'Cincinnati Royals'] },
  { id: 'SAS', name: 'San Antonio Spurs' },
  { id: 'TOR', name: 'Toronto Raptors' },
  { id: 'UTA', name: 'Utah Jazz' },
  { id: 'WAS', name: 'Washington Wizards', historicalNames: ['Washington Bullets'] },
];

export const TEAM_BY_ID: Record<string, Team> = Object.fromEntries(
  TEAMS.map((t) => [t.id, t]),
);

export function teamName(id: string): string {
  return TEAM_BY_ID[id]?.name ?? id;
}
