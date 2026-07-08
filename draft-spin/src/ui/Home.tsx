interface Props {
  resumable: boolean;
  onPlayFriend: () => void;
  onPlayAi: () => void;
  onResume: () => void;
}

const STEPS: [string, string][] = [
  ['Spin a category', 'The wheel lands on something like "Won an MVP" or "Played for the Bulls in the 90s".'],
  ['Type any NBA player', 'Search by name or nickname — KD, Bron, Shaq, T-Mac all work.'],
  ['Get fact-checked instantly', 'Right pick: he slots into your lineup. Wrong pick: ✕ — he’s crossed out and the turn passes on the same category. You always end with five.'],
  ['Battle in a best-of-7, then run it back', 'After 5 rounds your lineups (PG through Center) play a simulated series. Chain games back-to-back — every player already drafted is out of the pool.'],
];

export function HomeScreen({ resumable, onPlayFriend, onPlayAi, onResume }: Props) {
  return (
    <div className="stack fade-in">
      <header className="topbar">
        <div className="brand">You Know <em>Ball</em></div>
      </header>

      <div className="eyebrow">Head-to-head NBA draft showdown</div>
      <h1 className="headline">
        Spin. Type. <em>Get checked.</em> Prove you know ball.
      </h1>
      <p className="sub">
        Five rounds, one random category per round, every pick fact-checked against
        real career data — no arguing.
      </p>

      <button className="btn btn-primary" onClick={onPlayFriend}>
        Play a Friend
      </button>
      <button className="btn btn-primary btn-ai" onClick={onPlayAi}>
        🤖 Challenge the AI
      </button>
      {resumable && (
        <button className="btn btn-ghost" onClick={onResume}>
          Resume match
        </button>
      )}

      <section className="card">
        <div className="eyebrow" style={{ marginBottom: 8 }}>How it works</div>
        {STEPS.map(([title, body], i) => (
          <div className="how-step" key={title}>
            <div className="how-num">{i + 1}</div>
            <div>
              <b>{title}</b>
              <span>{body}</span>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
