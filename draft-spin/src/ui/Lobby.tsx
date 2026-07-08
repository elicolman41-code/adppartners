import { useState } from 'react';
import { AI_LEVELS, aiName, type AiLevel } from '../game/engine/ai';

interface Props {
  mode: 'friend' | 'ai';
  onStart: (you: string, friend: string, ai?: AiLevel) => void;
  onBack: () => void;
}

export function LobbyScreen({ mode, onStart, onBack }: Props) {
  const [you, setYou] = useState('');
  const [friend, setFriend] = useState('');
  const [level, setLevel] = useState<AiLevel>('veteran');

  const start = () => {
    if (mode === 'ai') onStart(you.trim() || 'You', aiName(level), level);
    else onStart(you.trim() || 'You', friend.trim() || 'Friend');
  };

  return (
    <div className="stack fade-in">
      <header className="topbar">
        <div className="brand">You Know <em>Ball</em></div>
      </header>

      <div className="eyebrow">New room</div>
      <h1 className="headline">{mode === 'ai' ? 'Pick your opponent' : 'Who’s playing?'}</h1>
      <p className="sub">
        {mode === 'ai'
          ? 'The bot drafts under the same rules you do — wrong picks get crossed out and the turn passes.'
          : 'Pass-and-play: you both use this phone. Player 1 picks first each round.'}
      </p>

      <div className="card stack">
        <div>
          <label className="field-label" htmlFor="you">{mode === 'ai' ? 'Your name' : 'Player 1'}</label>
          <input
            id="you"
            className="text-input"
            placeholder="You"
            maxLength={14}
            value={you}
            onChange={(e) => setYou(e.target.value)}
          />
        </div>
        {mode === 'friend' && (
          <div>
            <label className="field-label" htmlFor="friend">Player 2</label>
            <input
              id="friend"
              className="text-input"
              placeholder="Friend"
              maxLength={14}
              value={friend}
              onChange={(e) => setFriend(e.target.value)}
            />
          </div>
        )}
        {mode === 'ai' && (
          <div className="ai-levels">
            {AI_LEVELS.map((l) => (
              <button
                key={l.level}
                className={`ai-level ${level === l.level ? 'on' : ''}`}
                onClick={() => setLevel(l.level)}
              >
                <b>{l.name}</b>
                <span>{l.blurb}</span>
              </button>
            ))}
          </div>
        )}
      </div>

      <button className="btn btn-primary" onClick={start}>
        Create room &amp; start
      </button>
      <button className="btn btn-ghost" onClick={onBack}>
        Back
      </button>
    </div>
  );
}
