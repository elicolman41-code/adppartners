import type { Position } from '../types';
import { POSITION_ORDER } from '../types';
import { PLAYER_BY_ID } from '../data/db';

export interface Lineup {
  /** Starting-five slots in PG/SG/SF/PF/C order; null = open slot. */
  slots: Record<Position, string | null>;
  /** Players who couldn't get their own slot, tagged with their primary spot. */
  bench: { playerId: string; position: Position }[];
}

/**
 * Assign drafted players to the five lineup slots. Multi-position players
 * slide to wherever they're needed. Exhaustive search (≤5 players) maximizes
 * filled slots, then prefers everyone playing closer to their primary spot.
 */
export function buildLineup(playerIds: string[]): Lineup {
  const players = playerIds.filter((id) => PLAYER_BY_ID[id]);

  let bestAssign: (Position | null)[] = players.map(() => null);
  let bestFilled = -1;
  let bestPref = Infinity;

  const current: (Position | null)[] = players.map(() => null);
  const taken = new Set<Position>();

  const walk = (i: number, filled: number, pref: number) => {
    if (i === players.length) {
      if (filled > bestFilled || (filled === bestFilled && pref < bestPref)) {
        bestFilled = filled;
        bestPref = pref;
        bestAssign = [...current];
      }
      return;
    }
    const positions = PLAYER_BY_ID[players[i]].positions;
    for (let k = 0; k < positions.length; k++) {
      const pos = positions[k];
      if (taken.has(pos)) continue;
      taken.add(pos);
      current[i] = pos;
      walk(i + 1, filled + 1, pref + k);
      taken.delete(pos);
      current[i] = null;
    }
    walk(i + 1, filled, pref); // leave this player unassigned
  };
  walk(0, 0, 0);

  const slots: Record<Position, string | null> = { PG: null, SG: null, SF: null, PF: null, C: null };
  const bench: Lineup['bench'] = [];
  players.forEach((id, i) => {
    const pos = bestAssign[i];
    if (pos) slots[pos] = id;
    else bench.push({ playerId: id, position: PLAYER_BY_ID[id].positions[0] });
  });

  // Keep bench listed in lineup order for a tidy display.
  bench.sort((x, y) => POSITION_ORDER.indexOf(x.position) - POSITION_ORDER.indexOf(y.position));
  return { slots, bench };
}
