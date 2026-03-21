import React from 'react';

const CONFIG = {
  allowed:    { label: '✔ ALLOWED',    bg: 'rgba(0,255,136,0.12)',  border: 'var(--allowed-color)',    text: 'var(--allowed-color)' },
  suspicious: { label: '⚠ SUSPICIOUS', bg: 'rgba(255,214,10,0.12)', border: 'var(--suspicious-color)', text: 'var(--suspicious-color)' },
  blocked:    { label: '✖ BLOCKED',    bg: 'rgba(255,51,102,0.12)', border: 'var(--blocked-color)',    text: 'var(--blocked-color)' },
};

export default function StatusBadge({ status, large = false }) {
  const cfg = CONFIG[status] || CONFIG.suspicious;
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      padding: large ? '0.5rem 1.2rem' : '0.25rem 0.7rem',
      borderRadius: 6,
      border: `1px solid ${cfg.border}`,
      background: cfg.bg,
      color: cfg.text,
      fontFamily: 'var(--font-mono)',
      fontWeight: 700,
      fontSize: large ? '1rem' : '0.72rem',
      letterSpacing: '0.1em',
      boxShadow: large ? `0 0 20px ${cfg.bg}` : 'none',
    }}>
      {cfg.label}
    </span>
  );
}
