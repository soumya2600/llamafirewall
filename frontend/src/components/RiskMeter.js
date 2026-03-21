import React from 'react';

/**
 * RiskMeter — horizontal progress bar that changes color based on score.
 * score: 0.0 – 1.0
 */
export default function RiskMeter({ score }) {
  const pct = Math.round(score * 100);

  const color =
    score >= 0.7 ? 'var(--blocked-color)' :
    score >= 0.3 ? 'var(--suspicious-color)' :
    'var(--allowed-color)';

  const glow =
    score >= 0.7 ? 'rgba(255,51,102,0.6)' :
    score >= 0.3 ? 'rgba(255,214,10,0.5)' :
    'rgba(0,255,136,0.5)';

  return (
    <div>
      {/* Label row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--text-secondary)', letterSpacing: '0.08em' }}>
          RISK SCORE
        </span>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', fontWeight: 700, color }}>
          {score.toFixed(3)}
        </span>
      </div>

      {/* Track */}
      <div style={{
        width: '100%',
        height: 10,
        background: 'var(--bg-base)',
        borderRadius: 5,
        border: '1px solid var(--border)',
        overflow: 'hidden',
      }}>
        {/* Fill */}
        <div style={{
          width: `${pct}%`,
          height: '100%',
          background: color,
          boxShadow: `0 0 12px ${glow}`,
          borderRadius: 5,
          transition: 'width 0.6s cubic-bezier(0.4,0,0.2,1)',
        }} />
      </div>

      {/* Scale ticks */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.3rem' }}>
        {['0.0', '0.3', '0.7', '1.0'].map(t => (
          <span key={t} style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--text-dim)' }}>{t}</span>
        ))}
      </div>

      {/* Zone labels */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
        {[
          { label: '● SAFE',       color: 'var(--allowed-color)' },
          { label: '● SUSPICIOUS', color: 'var(--suspicious-color)' },
          { label: '● BLOCKED',    color: 'var(--blocked-color)' },
        ].map(z => (
          <span key={z.label} style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: z.color, letterSpacing: '0.08em' }}>
            {z.label}
          </span>
        ))}
      </div>
    </div>
  );
}
