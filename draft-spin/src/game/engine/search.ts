import type { Player } from '../types';
import { PLAYERS, latestTeamId } from '../data/db';
import { teamName } from '../data/teams';

/** Lowercase, strip accents, punctuation, and collapse spacing. */
export function normalizeName(input: string): string {
  return input
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[’'".,\-_]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

export interface SearchHit {
  player: Player;
  /** What matched: display name or a specific alias. */
  matchedOn: string;
  score: number;
}

interface IndexEntry {
  key: string;
  label: string;
  player: Player;
  isAlias: boolean;
}

const INDEX: IndexEntry[] = PLAYERS.flatMap((player) => [
  { key: normalizeName(player.displayName), label: player.displayName, player, isAlias: false },
  ...player.aliases.map((alias) => ({
    key: normalizeName(alias),
    label: alias,
    player,
    isAlias: true,
  })),
]);

/**
 * Autocomplete over display names + aliases. Exact matches first, then
 * prefix matches, then substring matches. Top `limit` unique players.
 */
export function searchPlayers(query: string, limit = 8): SearchHit[] {
  const q = normalizeName(query);
  if (q.length < 1) return [];

  const hits = new Map<string, SearchHit>();
  for (const entry of INDEX) {
    let score = 0;
    if (entry.key === q) score = 100;
    else if (entry.key.startsWith(q)) score = 60;
    else if (q.length >= 2 && entry.key.includes(q)) score = 30;
    else if (q.length >= 2) {
      // Also match last-name starts ("durant" -> Kevin Durant handled by
      // includes; "kd" style initials handled by aliases).
      const words = entry.key.split(' ');
      if (words.some((w) => w.startsWith(q))) score = 45;
    }
    if (score === 0) continue;
    if (entry.isAlias) score -= 2; // prefer real-name matches for ties
    if (!entry.player.active) score -= 1; // prefer current players for ties

    const existing = hits.get(entry.player.id);
    if (!existing || existing.score < score) {
      hits.set(entry.player.id, { player: entry.player, matchedOn: entry.label, score });
    }
  }

  return [...hits.values()]
    .sort((x, y) => y.score - x.score || x.player.displayName.localeCompare(y.player.displayName))
    .slice(0, limit);
}

/** Exact resolve for a submitted string (must match name or alias exactly). */
export function resolvePlayer(input: string): Player | null {
  const q = normalizeName(input);
  const exact = INDEX.find((e) => e.key === q);
  return exact ? exact.player : null;
}

export function playerSubtitle(player: Player): string {
  const status = player.active ? 'Active' : 'Retired';
  return `${player.position} · ${teamName(latestTeamId(player))} · ${status}`;
}
