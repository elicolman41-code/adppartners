import { useEffect, useState } from 'react';
import type { Match } from './game/types';
import { createMatch, loadMatch, saveMatch } from './game/engine/match';
import { HomeScreen } from './ui/Home';
import { LobbyScreen } from './ui/Lobby';
import { MatchScreen } from './ui/Match';

type View = 'home' | 'lobby' | 'match';

export default function App() {
  const [view, setView] = useState<View>('home');
  const [match, setMatch] = useState<Match | null>(() => loadMatch());

  useEffect(() => {
    saveMatch(match);
  }, [match]);

  const startMatch = (you: string, friend: string) => {
    setMatch(createMatch(you, friend));
    setView('match');
  };

  const quitMatch = () => {
    setMatch(null);
    setView('home');
  };

  return (
    <div className="app">
      {view === 'home' && (
        <HomeScreen
          resumable={match !== null}
          onPlay={() => setView('lobby')}
          onResume={() => setView('match')}
        />
      )}
      {view === 'lobby' && <LobbyScreen onStart={startMatch} onBack={() => setView('home')} />}
      {view === 'match' && match && (
        <MatchScreen match={match} setMatch={setMatch} onQuit={quitMatch} />
      )}

      <nav className="bottomnav">
        <button className={view === 'home' ? 'on' : ''} onClick={() => setView('home')}>
          <span className="ico">🏠</span>Home
        </button>
        <button
          className={view !== 'home' ? 'on' : ''}
          onClick={() => (match ? setView('match') : setView('lobby'))}
        >
          <span className="ico">🎰</span>Play
        </button>
      </nav>
    </div>
  );
}
