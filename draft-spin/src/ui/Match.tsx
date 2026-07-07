import { useEffect, useMemo, useRef, useState } from 'react';
import type { Match, Pick } from '../game/types';
import { CATEGORIES } from '../game/data/categories';
import { PLAYER_BY_ID } from '../game/data/db';
import { continueAfterReveal, spinForRound, submitPick } from '../game/engine/match';
import { playerSubtitle, searchPlayers } from '../game/engine/search';
import { ResultsScreen } from './Results';

interface Props {
  match: Match;
  setMatch: (m: Match) => void;
  onQuit: () => void;
}

export function MatchScreen({ match, setMatch, onQuit }: Props) {
  if (match.phase === 'results') {
    return <ResultsScreen match={match} onQuit={onQuit} />;
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

function ScoreBar({ match }: { match: Match }) {
  const [a, b] = match.participants;
  const picksThisRound = match.rounds[match.currentRound]?.picks ?? {};
  return (
    <div className="scorebar">
      <div className={`score-side ${match.turn === 0 && match.phase !== 'results' ? 'active' : ''}`}>
        <div className="name">{a.name}</div>
        <div className="pts">{a.score}</div>
      </div>
      <div className="score-mid">
        <div>RD {Math.min(match.currentRound + 1, match.totalRounds)}/{match.totalRounds}</div>
        <div className="round-dots">
          {Array.from({ length: match.totalRounds }, (_, i) => (
            <i
              key={i}
              className={
                i < match.currentRound || (i === match.currentRound && Object.keys(picksThisRound).length === 2)
                  ? 'done'
                  : ''
              }
            />
          ))}
        </div>
      </div>
      <div className={`score-side ${match.turn === 1 && match.phase !== 'results' ? 'active' : ''}`}>
        <div className="name">{b.name}</div>
        <div className="pts">{b.score}</div>
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
  const category = match.rounds[match.currentRound].category;
  const picker = match.participants[match.turn];

  const hits = useMemo(() => searchPlayers(query, 8), [query]);

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

      <div className="turn-banner">{picker.name} — your pick</div>

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
            {hits.map((h) => (
              <button key={h.player.id} className="suggestion" onClick={() => submit(h.player.displayName)}>
                <span>{h.player.displayName}</span>
                <small>{playerSubtitle(h.player)}</small>
              </button>
            ))}
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

function latestPick(match: Match): { pick: Pick; pickerName: string } | null {
  const round = match.rounds[match.currentRound];
  if (!round) return null;
  const entries = match.participants
    .map((pt) => ({ pick: round.picks[pt.id], pickerName: pt.name }))
    .filter((e): e is { pick: Pick; pickerName: string } => !!e.pick);
  if (entries.length === 0) return null;
  // With one pick, reveal it; with two, reveal the second picker's ruling.
  return entries.length === 1 ? entries[0] : entries[1];
}

function RevealPhase({ match, setMatch }: { match: Match; setMatch: (m: Match) => void }) {
  const latest = latestPick(match);
  if (!latest) {
    setMatch(continueAfterReveal(match));
    return null;
  }
  const { pick, pickerName } = latest;
  const player = PLAYER_BY_ID[pick.playerId];
  const kind = pick.outcome === 'eligible' ? 'ok' : pick.outcome === 'duplicate' ? 'dup' : 'bad';
  const title =
    pick.outcome === 'eligible' ? 'ELIGIBLE' : pick.outcome === 'duplicate' ? 'ALREADY DRAFTED' : 'NOT ELIGIBLE';

  const round = match.rounds[match.currentRound];
  const bothPicked = Object.keys(round.picks).length === 2;
  const isLastRound = match.currentRound === match.totalRounds - 1;
  const nextLabel = !bothPicked
    ? `Pass the phone — ${match.participants[match.turn].name} is up`
    : isLastRound
      ? 'Simulate the series'
      : 'Next round';

  return (
    <div className="stack fade-in">
      <div className={`verdict ${kind}`}>
        <div className="big">{title}</div>
        <div className="delta">{pick.points > 0 ? `+${pick.points}` : pick.points}</div>
        <div className="sub">
          {pickerName} picked <b style={{ color: 'var(--text)' }}>{player?.displayName}</b>
          {' · '}
          {round.category.label}
        </div>
        <div className="reason">{pick.reason}</div>
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

function Rosters({ match }: { match: Match }) {
  return (
    <div className="card">
      <div className="eyebrow" style={{ marginBottom: 10 }}>Rosters</div>
      <div className="roster-grid">
        {match.participants.map((pt) => (
          <div className="roster-col" key={pt.id}>
            <h4>{pt.name}</h4>
            {Array.from({ length: match.totalRounds }, (_, i) => {
              const id = pt.roster[i];
              return id ? (
                <div className="roster-slot filled" key={i}>
                  {PLAYER_BY_ID[id]?.displayName ?? id}
                </div>
              ) : (
                <div className="roster-slot empty" key={i}>
                  Slot {i + 1}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
