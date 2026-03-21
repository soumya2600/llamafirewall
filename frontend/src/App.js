import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import CheckPage from './components/CheckPage';
import LogsPage from './components/LogsPage';
import { pingBackend, fetchStatus, BASE_URL } from './api';

export default function App() {
  const [page, setPage]               = useState('check');
  const [backendStatus, setBackendStatus] = useState('checking');
  const [engineStatus, setEngineStatus]   = useState(null);
  // engineStatus: { ai_mode: "cloud"|"local"|"none", model: "...", mode_label: "..." }

  useEffect(() => {
    async function check() {
      const ok = await pingBackend();
      setBackendStatus(ok ? 'online' : 'offline');
      if (ok) {
        const s = await fetchStatus();
        setEngineStatus(s);
      }
    }
    check();
    const interval = setInterval(check, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header
        page={page} setPage={setPage}
        backendStatus={backendStatus}
        engineStatus={engineStatus}
      />
      <main style={{ flex: 1, padding: '2rem 1rem', maxWidth: 900, margin: '0 auto', width: '100%' }}>
        {page === 'check'
          ? <CheckPage backendStatus={backendStatus} engineStatus={engineStatus} />
          : <LogsPage  backendStatus={backendStatus} />}
      </main>
      <footer style={{
        textAlign: 'center', padding: '1.2rem',
        color: 'var(--text-dim)', fontFamily: 'var(--font-mono)',
        fontSize: '0.72rem', borderTop: '1px solid var(--border)',
        display: 'flex', justifyContent: 'center', gap: '1.5rem', flexWrap: 'wrap',
      }}>
        <span>AI ASSISTANT FIREWALL v2.1</span>
        <span>BACKEND: <span style={{ color: backendStatus === 'online' ? 'var(--neon-green)' : 'var(--neon-red)' }}>{backendStatus.toUpperCase()}</span></span>
        {engineStatus && (
          <span>ENGINE: <span style={{ color: engineStatus.ai_mode === 'none' ? 'var(--text-dim)' : '#a855f7' }}>{engineStatus.mode_label?.toUpperCase()}</span></span>
        )}
      </footer>
    </div>
  );
}
