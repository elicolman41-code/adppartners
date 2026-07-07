import { useState } from 'react';

interface Props {
  onStart: (you: string, friend: string) => void;
  onBack: () => void;
}

export function LobbyScreen({ onStart, onBack }: Props) {
  const [you, setYou] = useState('');
  const [friend, setFriend] = useState('');

  return (
    <div className="stack fade-in">
      <header className="topbar">
        <div className="brand">Draft<em>Spin</em></div>
      </header>

      <div className="eyebrow">New room</div>
      <h1 className="headline">Who’s playing?</h1>
      <p className="sub">
        Pass-and-play: you both use this phone. Player 1 picks first each round.
      </p>

      <div className="card stack">
        <div>
          <label className="field-label" htmlFor="you">Player 1</label>
          <input
            id="you"
            className="text-input"
            placeholder="You"
            maxLength={14}
            value={you}
            onChange={(e) => setYou(e.target.value)}
          />
        </div>
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
      </div>

      <button className="btn btn-primary" onClick={() => onStart(you.trim() || 'You', friend.trim() || 'Friend')}>
        Create room &amp; start
      </button>
      <button className="btn btn-ghost" onClick={onBack}>
        Back
      </button>
    </div>
  );
}
