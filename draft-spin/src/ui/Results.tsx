import { useMemo } from 'react';
import type { Match } from '../game/types';
import { PLAYER_BY_ID } from '../game/data/db';
import { WIN_SERIES_BONUS } from '../game/engine/match';
import { simulateSeries } from '../game/engine/simulator';

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

  // The +3 series bonus is applied at display time so a reload never
  // double-counts it in the saved match state.
  const finalScores = match.participants.map((pt, i) =>
    i === series.winnerSide ? pt.score + WIN_SERIES_BONUS : pt.score,
  );
  const champion =
    finalScores[0] === finalScores[1]
      ? null
      : match.participants[finalScores[0] > finalScores[1] ? 0 : 1];

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
          {' · '}+{WIN_SERIES_BONUS} bonus
        </div>
      </div>

      <div className="card">
        <div className="eyebrow" style={{ marginBottom: 6 }}>Final points</div>
        <div className="roster-grid">
          {match.participants.map((pt, i) => (
            <div className="score-side" key={pt.id} style={{ textAlign: 'center' }}>
              <div className="name">{pt.name}</div>
              <div className="pts">{finalScores[i]}</div>
            </div>
          ))}
        </div>
        <p className="sub" style={{ textAlign: 'center', marginTop: 8 }}>
          {champion ? `${champion.name} takes the match.` : 'Dead even — run it back.'}
        </p>
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
        <div className="eyebrow" style={{ marginBottom: 10 }}>Final rosters</div>
        <div className="roster-grid">
          {match.participants.map((pt) => (
            <div className="roster-col" key={pt.id}>
              <h4>{pt.name}</h4>
              {pt.roster.length === 0 && <div className="roster-slot empty">No eligible picks</div>}
              {pt.roster.map((id) => (
                <div className="roster-slot filled" key={id}>
                  {PLAYER_BY_ID[id]?.displayName ?? id}
                </div>
              ))}
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
