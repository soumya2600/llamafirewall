import React, { useState, useEffect } from 'react';
import { fetchLogs, clearLogs } from '../api';
import StatusBadge from './StatusBadge';

const card = {
  background: 'var(--bg-card)', border: '1px solid var(--border)',
  borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem',
};

export default function LogsPage({ backendStatus }) {
  const [logs, setLogs]         = useState([]);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState('');
  const [clearing, setClearing] = useState(false);

  async function load() {
    if (backendStatus === 'offline') {
      setError('Backend is offline. Start the server to view logs.');
      setLoading(false);
      return;
    }
    setLoading(true); setError('');
    try {
      const data = await fetchLogs();
      setLogs(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleClear() {
    if (!window.confirm('Clear all logs from the database?')) return;
    setClearing(true);
    try {
      await clearLogs();
      setLogs([]);
    } catch (e) {
      setError(e.message);
    } finally {
      setClearing(false);
    }
  }

  useEffect(() => { load(); }, [backendStatus]);

  const total      = logs.length;
  const blocked    = logs.filter(l => l.status === 'blocked').length;
  const suspicious = logs.filter(l => l.status === 'suspicious').length;
  const allowed    = logs.filter(l => l.status === 'allowed').length;

  return (
    <div className="fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontFamily: 'var(--font-display)', fontWeight: 900, fontSize: '1.5rem', letterSpacing: '0.06em', textTransform: 'uppercase', color: 'var(--neon-blue)' }}>
            Logs Dashboard
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', fontSize: '0.75rem', letterSpacing: '0.05em' }}>
            {backendStatus === 'online' ? '✔ LIVE DATA FROM SQLITE DATABASE' : '✖ BACKEND OFFLINE'}
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button onClick={load}       style={btnStyle('var(--neon-blue)')}>↻ Refresh</button>
          <button onClick={handleClear} disabled={clearing || backendStatus !== 'online'} style={btnStyle('var(--neon-red)')}>
            {clearing ? '…' : '🗑 Clear All'}
          </button>
        </div>
      </div>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
        <StatCard label="TOTAL SCANS"  value={total}      color="var(--neon-blue)" />
        <StatCard label="ALLOWED"       value={allowed}    color="var(--allowed-color)" />
        <StatCard label="SUSPICIOUS"    value={suspicious} color="var(--suspicious-color)" />
        <StatCard label="BLOCKED"       value={blocked}    color="var(--blocked-color)" />
      </div>

      {/* Table */}
      <div style={card}>
        {error && (
          <div style={{ color: 'var(--neon-red)', fontFamily: 'var(--font-mono)', fontSize: '0.8rem', marginBottom: '1rem' }}>
            ⚠ {error}
          </div>
        )}
        {loading ? (
          <div style={{ textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', padding: '2rem' }}>Loading from database…</div>
        ) : logs.length === 0 ? (
          <div style={{ textAlign: 'center', color: 'var(--text-dim)', fontFamily: 'var(--font-mono)', padding: '2rem' }}>
            {backendStatus === 'online' ? 'No logs yet. Analyze some prompts first.' : 'Start the backend to see logs.'}
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--font-mono)', fontSize: '0.78rem' }}>
              <thead>
                <tr>
                  {['#', 'Prompt', 'Risk Score', 'Status', 'Timestamp'].map(h => (
                    <th key={h} style={{ padding: '0.6rem 0.8rem', textAlign: 'left', color: 'var(--neon-blue)', letterSpacing: '0.08em', borderBottom: '1px solid var(--border)', whiteSpace: 'nowrap' }}>
                      {h.toUpperCase()}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {logs.map(log => (
                  <tr key={log.id} style={{ borderBottom: '1px solid var(--border)', transition: 'background 0.15s' }}
                    onMouseOver={e => e.currentTarget.style.background = 'rgba(0,212,255,0.04)'}
                    onMouseOut={e  => e.currentTarget.style.background = 'transparent'}
                  >
                    <td style={{ padding: '0.7rem 0.8rem', color: 'var(--text-dim)' }}>{log.id}</td>
                    <td style={{ padding: '0.7rem 0.8rem', color: 'var(--text-primary)', maxWidth: 260 }}>
                      <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={log.prompt}>{log.prompt}</div>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-dim)', marginTop: '0.2rem', whiteSpace: 'normal', lineHeight: 1.4 }}>{log.reason}</div>
                    </td>
                    <td style={{ padding: '0.7rem 0.8rem' }}>
                      <span style={{ color: log.risk_score >= 0.7 ? 'var(--blocked-color)' : log.risk_score >= 0.3 ? 'var(--suspicious-color)' : 'var(--allowed-color)', fontWeight: 700 }}>
                        {parseFloat(log.risk_score).toFixed(3)}
                      </span>
                    </td>
                    <td style={{ padding: '0.7rem 0.8rem' }}><StatusBadge status={log.status} /></td>
                    <td style={{ padding: '0.7rem 0.8rem', color: 'var(--text-dim)', whiteSpace: 'nowrap' }}>
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({ label, value, color }) {
  return (
    <div style={{ background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 10, padding: '1rem', textAlign: 'center' }}>
      <div style={{ fontSize: '2rem', fontWeight: 900, fontFamily: 'var(--font-display)', color }}>{value}</div>
      <div style={{ fontSize: '0.65rem', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)', letterSpacing: '0.1em', marginTop: '0.2rem' }}>{label}</div>
    </div>
  );
}

function btnStyle(color) {
  return {
    padding: '0.45rem 1rem', background: 'transparent',
    border: `1px solid ${color}`, borderRadius: 6, color,
    fontFamily: 'var(--font-mono)', fontSize: '0.78rem',
    cursor: 'pointer', letterSpacing: '0.05em',
  };
}
