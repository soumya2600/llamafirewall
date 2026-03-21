import React from 'react';

const MODE_COLORS = {
  cloud: '#a855f7',
  local: '#00d4ff',
  none:  '#475569',
};
const MODE_LABELS = {
  cloud: '☁ Cloud AI',
  local: '🖥 Local AI',
  none:  '⚙ Rules Only',
};

function ConnPill({ status }) {
  const cfg = {
    online:   { color: 'var(--neon-green)',  label: '● LIVE' },
    offline:  { color: 'var(--neon-red)',    label: '● OFFLINE' },
    checking: { color: 'var(--text-dim)',    label: '○ …' },
  }[status] || {};
  return (
    <div style={{
      padding: '0.3rem 0.8rem', borderRadius: 20,
      border: `1px solid ${cfg.color}`, color: cfg.color,
      fontFamily: 'var(--font-mono)', fontSize: '0.68rem', letterSpacing: '0.08em',
    }}>{cfg.label}</div>
  );
}

function EngineChip({ engineStatus }) {
  if (!engineStatus) return null;
  const mode  = engineStatus.ai_mode || 'none';
  const color = MODE_COLORS[mode];
  const label = MODE_LABELS[mode];
  const model = engineStatus.model ? ` · ${engineStatus.model}` : '';
  return (
    <div style={{
      padding: '0.3rem 0.9rem', borderRadius: 20,
      border: `1px solid ${color}`, color,
      fontFamily: 'var(--font-mono)', fontSize: '0.68rem', letterSpacing: '0.06em',
      maxWidth: 260, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
    }} title={`${label}${model}`}>
      {label}{model}
    </div>
  );
}

function NavBtn({ label, active, onClick }) {
  return (
    <button onClick={onClick} style={{
      padding: '0.45rem 1.1rem', borderRadius: 6,
      border: active ? '1px solid var(--neon-blue)' : '1px solid var(--border)',
      background: active ? 'rgba(0,212,255,0.12)' : 'transparent',
      color: active ? 'var(--neon-blue)' : 'var(--text-secondary)',
      fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: '0.85rem',
      cursor: 'pointer', letterSpacing: '0.05em', textTransform: 'uppercase', transition: 'all 0.2s',
    }}>{label}</button>
  );
}

export default function Header({ page, setPage, backendStatus, engineStatus }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border)', background: 'rgba(5,8,16,0.97)',
      backdropFilter: 'blur(12px)', position: 'sticky', top: 0, zIndex: 100,
    }}>
      <div style={{
        maxWidth: 900, margin: '0 auto', padding: '1rem 1.5rem',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        flexWrap: 'wrap', gap: '0.75rem',
      }}>
        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: 38, height: 38, background: 'linear-gradient(135deg, #1e3a8a, #7e22ce)',
            borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.2rem', boxShadow: '0 0 20px rgba(0,212,255,0.3)',
          }}>🛡️</div>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: '1.15rem', letterSpacing: '0.05em', color: 'var(--neon-blue)', textTransform: 'uppercase' }}>AI Firewall</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.62rem', color: 'var(--text-dim)', letterSpacing: '0.1em' }}>PROMPT SECURITY SYSTEM</div>
          </div>
        </div>

        {/* Right side */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
          <ConnPill status={backendStatus} />
          <EngineChip engineStatus={engineStatus} />
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <NavBtn label="⚡ Scan" active={page === 'check'} onClick={() => setPage('check')} />
            <NavBtn label="📋 Logs" active={page === 'logs'}  onClick={() => setPage('logs')} />
          </div>
        </div>
      </div>
    </header>
  );
}
