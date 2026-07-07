import { useEffect, useMemo, useRef, useState } from 'react';
import type { Match } from '../game/types';
import { POSITION_NAMES, POSITION_ORDER } from '../game/types';
import { CATEGORIES } from '../game/data/categories';
import { PLAYER_BY_ID } from '../game/data/db';
import {
  continueAfterReveal,
  roundComplete,
  roundMarks,
  spinForRound,
  submitPick,
  unavailableIds,
} from '../game/engine/match';
import { buildLineup } from '../game/engine/lineup';
import { playerSubtitle, searchPlayers } from '../game/engine/search';
import { ResultsScreen } from './Results';

interface Props {
  match: Match;
  setMatch: (m: Match) => void;
  onRunItBack: (winnerSide: 0 | 1) => void;
  onQuit: () => void;
}

export function MatchScreen({ match, setMatch, onRunItBack, onQuit }: Props) {
  if (match.phase === 'results') {
    return <ResultsScreen match={match} onRunItBack={onRunItBack} onQuit={onQuit} />;
  }
  return (
    <div className="stack fade-in">
      <header className="topbar">
        <div className="brand">Draft<em>Spin</em></div>
        <div className="room-chip">ROOM {match.roomCode}</div>
      </header>

      <ScoreBar match={match} />

      {match.phase === 'spin' && <SpinPhase match={match} setMatch={setMatch} />}
      {match.phase === 'pick' && <PickPhase match={match} setMatch={setMatch} />}
      {match.phase === 'reveal' && <RevealPhase match={match} setMatch={setMatch} />}

      <Rosters match={match} />
    </div>
  );
}

export function MarkStrip({ marks }: { marks: ReturnType<typeof roundMarks> }) {
  return (
    <div className="mark-strip">
      {marks.map((m, i) => {
        const cls = m.landed ? 'hit' : m.misses > 0 ? 'x' : 'pending';
        return (
          <span key={i} className={`mark ${cls}`}>
            {m.landed ? '✓' : m.misses > 0 ? '✕' : '·'}
            {m.misses > 0 && <i className="mark-misses">{m.misses}</i>}
          </span>
        );
      })}
    </div>
  );
}

function ScoreBar({ match }: { match: Match }) {
  const [a, b] = match.participants;
  const inRun = match.game > 1;
  return (
    <div className="scorebar">
      <div className={`score-side ${match.turn === 0 && match.phase !== 'results' ? 'active' : ''}`}>
        <div className="name">{a.name}</div>
        <MarkStrip marks={roundMarks(match, 0)} />
      </div>
      <div className="score-mid">
        <div>RD {Math.min(match.currentRound + 1, match.totalRounds)}/{match.totalRounds}</div>
        {inRun && (
          <div className="run-chip">
            GM {match.game} · {match.runWins[0]}–{match.runWins[1]}
          </div>
        )}
      </div>
      <div className={`score-side ${match.turn === 1 && match.phase !== 'results' ? 'active' : ''}`}>
        <div className="name">{b.name}</div>
        <MarkStrip marks={roundMarks(match, 1)} />
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Spin phase — slot-machine roll that settles on the deterministic category.
// ---------------------------------------------------------------------------

function SpinPhase({ match, setMatch }: { match: Match; setMatch: (m: Match) => void }) {
  const [rolling, setRolling] = useState(false);
  const [rollLabel, setRollLabel] = useState('Ready?');
  const timers = useRef<number[]>([]);

  useEffect(() => () => timers.current.forEach(clearTimeout), []);

  const spin = () => {
    if (rolling) return;
    setRolling(true);
    const { match: next, category } = spinForRound(match);

    // Roll through decoy labels, slowing down, then settle on the real one.
    const decoys = CATEGORIES.filter((c) => c.id !== category.definitionId).map((c) =>
      c.label.replace('{team}', 'Lakers').replace('{decade}', '1990'),
    );
    let delay = 0;
    const steps = 14;
    for (let i = 0; i < steps; i++) {
      delay += 45 + i * 14;
      const label = decoys[Math.floor(Math.random() * decoys.length)];
      timers.current.push(window.setTimeout(() => setRollLabel(label), delay));
    }
    timers.current.push(
      window.setTimeout(() => {
        setRollLabel(category.label);
        setRolling(false);
        setMatch(next);
      }, delay + 260),
    );
  };

  return (
    <div className="stack">
      <div className="spin-window">
        <div className="spin-tag">Round {match.currentRound + 1} category</div>
        <div className={`spin-label ${rolling ? 'rolling' : ''}`}>{rollLabel}</div>
      </div>
      <button className="btn btn-primary" onClick={spin} disabled={rolling}>
        {rolling ? 'Spinning…' : 'Spin the category'}
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Pick phase — alias-aware autocomplete, typo forgiveness.
// ---------------------------------------------------------------------------

function PickPhase({ match, setMatch }: { match: Match; setMatch: (m: Match) => void }) {
  const [query, setQuery] = useState('');
  const [typoInput, setTypoInput] = useState<string | null>(null);
  const round = match.rounds[match.currentRound];
  const category = round.category;
  const picker = match.participants[match.turn];

  const hits = useMemo(() => searchPlayers(query, 8), [query]);
  // Out of the pool: drafted this run/game, or crossed out earlier this round.
  const gone = useMemo(() => {
    const s = unavailableIds(match);
    for (const a of round.attempts) s.add(a.pick.playerId);
    return s;
  }, [match, round]);
  const myMisses = roundMarks(match, match.turn)[match.currentRound].misses;

  const submit = (input: string) => {
    const out = submitPick(match, input);
    if (out.kind === 'unknown') {
      setTypoInput(input);
      return;
    }
    setTypoInput(null);
    setQuery('');
    setMatch(out.match);
  };

  return (
    <div className="stack">
      <div className="spin-window">
        <div className="spin-tag">Round {match.currentRound + 1} category</div>
        <div className="spin-label settled">{category.label}</div>
      </div>

      <div className="turn-banner">
        {picker.name} — {myMisses > 0 ? 'back on the clock, land one this time' : 'your pick'}
      </div>

      <div className="search-wrap">
        <input
          className="search-input"
          placeholder="Type any NBA player…"
          value={query}
          autoComplete="off"
          autoCorrect="off"
          spellCheck={false}
          onChange={(e) => {
            setQuery(e.target.value);
            setTypoInput(null);
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && query.trim()) submit(query);
          }}
        />
        {query.trim().length > 0 && hits.length > 0 && (
          <div className="suggestions">
            {hits.map((h) => {
              const taken = gone.has(h.player.id);
              const crossedOut = round.attempts.some(
                (a) => a.pick.playerId === h.player.id && a.pick.outcome !== 'eligible',
              );
              return (
                <button
                  key={h.player.id}
                  className={`suggestion ${taken ? 'taken' : ''}`}
                  disabled={taken}
                  onClick={() => submit(h.player.displayName)}
                >
                  <span>{h.player.displayName}</span>
                  <small>
                    {crossedOut
                      ? 'Crossed out this round'
                      : taken
                        ? 'Already drafted — out of the pool'
                        : playerSubtitle(h.player)}
                  </small>
                </button>
              );
            })}
          </div>
        )}
      </div>

      <button className="btn btn-primary" onClick={() => submit(query)} disabled={!query.trim()}>
        Submit pick
      </button>

      {typoInput !== null && (
        <p className="typo-note">
          🤔 No player found for <b>“{typoInput}”</b>. No penalty — check the spelling or tap a
          suggestion.
        </p>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Reveal phase — the ruling, the evidence, the penalty.
// ---------------------------------------------------------------------------

function RevealPhase({ match, setMatch }: { match: Match; setMatch: (m: Match) => void }) {
  const round = match.rounds[match.currentRound];
  const latest = round?.attempts[round.attempts.length - 1];
  // Reveal with nothing to reveal (corrupted save): advance via effect, never
  // set state during render.
  useEffect(() => {
    if (!latest) setMatch(continueAfterReveal(match));
  }, [latest, match, setMatch]);
  if (!latest) return null;
  const { pick } = latest;
  const picker = match.participants.find((pt) => pt.id === latest.participantId)!;
  const player = PLAYER_BY_ID[pick.playerId];
  const kind = pick.outcome === 'eligible' ? 'ok' : pick.outcome === 'duplicate' ? 'dup' : 'bad';
  const title =
    pick.outcome === 'eligible' ? 'ELIGIBLE' : pick.outcome === 'duplicate' ? 'ALREADY DRAFTED' : 'NOT ELIGIBLE';

  const done = roundComplete(match, match.currentRound);
  const isLastRound = match.currentRound === match.totalRounds - 1;
  const nextPicker = match.participants[match.turn];
  const samePicker = nextPicker.id === picker.id;
  const nextLabel = !done
    ? samePicker
      ? `${nextPicker.name} — take another shot`
      : `Pass the phone — ${nextPicker.name} is up`
    : isLastRound
      ? 'Simulate the series'
      : 'Next round';
  const xNote = samePicker
    ? `${player?.displayName} is crossed out — ${nextPicker.name} stays on the clock. Same category, another shot.`
    : `${player?.displayName} is crossed out — ${nextPicker.name} takes over on the same category. Nobody loses a spot: everyone still ends with five.`;

  return (
    <div className="stack fade-in">
      <div className={`verdict ${kind}`}>
        <div className="delta">{pick.outcome === 'eligible' ? '✓' : '✕'}</div>
        <div className="big">{title}</div>
        <div className="sub">
          {picker.name} picked <b style={{ color: 'var(--text)' }}>{player?.displayName}</b>
          {' · '}
          {round.category.label}
        </div>
        <div className="reason">{pick.reason}</div>
        {pick.outcome !== 'eligible' && <div className="x-note">{xNote}</div>}
      </div>

      <div className="card evidence">
        <div className="eyebrow" style={{ marginBottom: 4 }}>The ruling</div>
        {pick.evidence.map((e, i) => (
          <div className="evidence-row" key={i}>
            <span className="f">{e.field}</span>
            <span className="v">
              needs {e.expected} · has {e.actual}
            </span>
          </div>
        ))}
        <div className="evidence-note">{pick.evidence[0]?.sourceNote}</div>
      </div>

      <button className="btn btn-primary" onClick={() => setMatch(continueAfterReveal(match))}>
        {nextLabel}
      </button>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Rosters
// ---------------------------------------------------------------------------

export function LineupCard({ playerIds }: { playerIds: string[] }) {
  const lineup = useMemo(() => buildLineup(playerIds), [playerIds]);
  return (
    <>
      {POSITION_ORDER.map((pos) => {
        const id = lineup.slots[pos];
        const player = id ? PLAYER_BY_ID[id] : null;
        return (
          <div className={`lineup-slot ${player ? 'filled' : 'empty'}`} key={pos}>
            <span className="lineup-pos">{POSITION_NAMES[pos]}</span>
            <span className="lineup-player">
              {player ? player.displayName : '—'}
              {player && player.positions.length > 1 && (
                <small className="lineup-flex"> {player.positions.join('/')}</small>
              )}
            </span>
          </div>
        );
      })}
      {lineup.bench.map(({ playerId, position }) => (
        <div className="lineup-slot filled bench" key={playerId}>
          <span className="lineup-pos">Bench · {POSITION_NAMES[position]}</span>
          <span className="lineup-player">{PLAYER_BY_ID[playerId]?.displayName}</span>
        </div>
      ))}
    </>
  );
}

function Rosters({ match }: { match: Match }) {
  return (
    <div className="card">
      <div className="eyebrow" style={{ marginBottom: 10 }}>Lineups</div>
      <div className="roster-grid">
        {match.participants.map((pt) => (
          <div className="roster-col" key={pt.id}>
            <h4>{pt.name}</h4>
            <LineupCard playerIds={pt.roster} />
          </div>
        ))}
      </div>
    </div>
  );
}
