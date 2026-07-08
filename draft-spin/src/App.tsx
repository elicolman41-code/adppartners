import { useEffect, useState } from 'react';
import type { Match } from './game/types';
import type { AiLevel } from './game/engine/ai';
import { createMatch, loadMatch, rematch, saveMatch } from './game/engine/match';
import { HomeScreen } from './ui/Home';
import { LobbyScreen } from './ui/Lobby';
import { MatchScreen } from './ui/Match';

type View = 'home' | 'lobby' | 'match';

export default function App() {
  const [view, setView] = useState<View>('home');
  const [lobbyMode, setLobbyMode] = useState<'friend' | 'ai'>('friend');
  const [match, setMatch] = useState<Match | null>(() => loadMatch());

  useEffect(() => {
    saveMatch(match);
  }, [match]);

  const startMatch = (you: string, friend: string, ai?: AiLevel) => {
    setMatch(createMatch(you, friend, ai));
    setView('match');
  };

  const quitMatch = () => {
    setMatch(null);
    setView('home');
  };

  const runItBack = (winnerSide: 0 | 1) => {
    if (match) setMatch(rematch(match, winnerSide));
  };

  return (
    <div className="app">
      {view === 'home' && (
        <HomeScreen
          resumable={match !== null}
          onPlayFriend={() => { setLobbyMode('friend'); setView('lobby'); }}
          onPlayAi={() => { setLobbyMode('ai'); setView('lobby'); }}
          onResume={() => setView('match')}
        />
      )}
      {view === 'lobby' && (
        <LobbyScreen mode={lobbyMode} onStart={startMatch} onBack={() => setView('home')} />
      )}
      {view === 'match' && match && (
        <MatchScreen match={match} setMatch={setMatch} onRunItBack={runItBack} onQuit={quitMatch} />
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
