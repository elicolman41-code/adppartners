import { useMemo } from 'react';
import type { Match } from '../game/types';
import { PLAYER_BY_ID } from '../game/data/db';
import { roundMarks } from '../game/engine/match';
import { simulateSeries } from '../game/engine/simulator';
import { LineupCard } from './Match';

interface Props {
  match: Match;
  onQuit: () => void;
}

export function ResultsScreen({ match, onQuit }: Props) {
  const [a, b] = match.participants;

  // Seeded by match id — reloading the room shows the identical series.
  const series = useMemo(
    () => simulateSeries(match.id, [a.roster, b.roster], [a.name, b.name]),
    [match.id, a.roster, b.roster, a.name, b.name],
  );

  const winner = match.participants[series.winnerSide];
  const mvp = PLAYER_BY_ID[series.mvpPlayerId];

  return (
    <div className="stack fade-in">
      <header className="topbar">
        <div className="brand">Draft<em>Spin</em></div>
        <div className="room-chip">ROOM {match.roomCode}</div>
      </header>

      <div className="card series-hero">
        <div className="trophy">🏆</div>
        <div className="winner">{winner.name} wins the series</div>
        <div className="scoreline">
          {series.wins[series.winnerSide]}–{series.wins[1 - series.winnerSide]}
        </div>
      </div>

      <div className="card">
        <div className="eyebrow" style={{ marginBottom: 6 }}>Draft report</div>
        <div className="roster-grid">
          {match.participants.map((pt, i) => (
            <div className="score-side" key={pt.id} style={{ textAlign: 'center' }}>
              <div className="name">{pt.name}</div>
              <div className="mark-strip center">
                {roundMarks(match, i as 0 | 1).map((m, r) => (
                  <span key={r} className={`mark ${m}`}>{m === 'hit' ? '✓' : m === 'x' ? '✕' : '·'}</span>
                ))}
              </div>
              <div className="sub">{pt.roster.length}/5 picks landed</div>
            </div>
          ))}
        </div>
      </div>

      <div className="card mvp-row">
        <div className="mvp-badge">⭐</div>
        <div>
          <div className="eyebrow">Series MVP</div>
          <b style={{ fontSize: 17 }}>{mvp?.displayName ?? '—'}</b>
        </div>
      </div>

      <div className="card">
        <div className="eyebrow" style={{ marginBottom: 4 }}>The series</div>
        {series.games.map((g) => (
          <div className="game-row" key={g.index}>
            <span className="g">G{g.index}</span>
            <span className="s">
              {match.participants[g.winnerSide].name} {g.scores[g.winnerSide]}–{g.scores[1 - g.winnerSide]}
            </span>
            <span className="note">{g.closingNote}</span>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="eyebrow" style={{ marginBottom: 4 }}>Why {winner.name} won</div>
        <ul className="why-list">
          {series.whyRundown.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </div>

      <div className="card">
        <div className="eyebrow" style={{ marginBottom: 10 }}>Final lineups</div>
        <div className="roster-grid">
          {match.participants.map((pt) => (
            <div className="roster-col" key={pt.id}>
              <h4>{pt.name}</h4>
              <LineupCard playerIds={pt.roster} />
            </div>
          ))}
        </div>
      </div>

      <button className="btn btn-primary" onClick={onQuit}>
        Play again
      </button>
    </div>
  );
}
