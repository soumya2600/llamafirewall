import React, { useState } from 'react';
import { checkPrompt } from '../api';
import RiskMeter from './RiskMeter';
import StatusBadge from './StatusBadge';
import { SAMPLE_PROMPTS } from '../samplePrompts';

const card = {
  background: 'var(--bg-card)', border: '1px solid var(--border)',
  borderRadius: 12, padding: '1.5rem', marginBottom: '1.5rem',
};

export default function CheckPage({ backendStatus }) {
  const [prompt, setPrompt]   = useState('');
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  async function handleCheck() {
    if (!prompt.trim()) { setError('Please enter a prompt.'); return; }
    if (backendStatus === 'offline') {
      setError('Backend is offline. Start the FastAPI server first: uvicorn main:app --reload');
      return;
    }
    setError(''); setLoading(true); setResult(null);
    try {
      const data = await checkPrompt(prompt);
      setResult(data);
    } catch (e) {
      setError(e.message || 'Failed to connect to backend. Is it running on port 8000?');
    } finally {
      setLoading(false);
    }
  }

  // Allow Enter key (Ctrl+Enter) to submit
  function handleKeyDown(e) {
    if (e.ctrlKey && e.key === 'Enter') handleCheck();
  }

  function loadSample(s) {
    setPrompt(s.prompt); setResult(null); setError('');
  }

  const statusColor = {
    online:   'var(--neon-green)',
    offline:  'var(--neon-red)',
    checking: 'var(--text-dim)',
  }[backendStatus];

  return (
    <div className="fade-in">
      {/* Hero */}
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{
          fontFamily: 'var(--font-display)', fontWeight: 900,
          fontSize: 'clamp(1.6rem, 4vw, 2.4rem)', letterSpacing: '0.06em',
          textTransform: 'uppercase',
          background: 'linear-gradient(90deg, var(--neon-blue), var(--neon-purple))',
          WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          marginBottom: '0.5rem',
        }}>
          Prompt Security Scanner
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontFamily: 'var(--font-mono)', letterSpacing: '0.05em' }}>
          DETECT · SCORE · BLOCK MALICIOUS AI INPUTS IN REAL-TIME
        </p>
      </div>

      {/* Input */}
      <div style={card}>
        <label style={{ display: 'block', fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--neon-blue)', letterSpacing: '0.1em', marginBottom: '0.6rem' }}>
          PROMPT INPUT &nbsp;<span style={{ color: 'var(--text-dim)', fontSize: '0.65rem' }}>(Ctrl+Enter to submit)</span>
        </label>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={5}
          placeholder="Enter a user prompt to analyze for security threats…"
          style={{
            width: '100%', background: 'var(--bg-input)',
            border: '1px solid var(--border)', borderRadius: 8,
            padding: '0.9rem', color: 'var(--text-primary)',
            fontFamily: 'var(--font-mono)', fontSize: '0.88rem',
            resize: 'vertical', outline: 'none', transition: 'border-color 0.2s',
          }}
          onFocus={e => e.target.style.borderColor = 'var(--neon-blue)'}
          onBlur={e  => e.target.style.borderColor = 'var(--border)'}
        />

        {error && (
          <div style={{ marginTop: '0.5rem', color: 'var(--neon-red)', fontFamily: 'var(--font-mono)', fontSize: '0.78rem', lineHeight: 1.5 }}>
            ⚠ {error}
          </div>
        )}

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <button
            onClick={handleCheck}
            disabled={loading || backendStatus === 'checking'}
            style={{
              padding: '0.7rem 2rem',
              background: (loading || backendStatus !== 'online') ? 'var(--border)' : 'linear-gradient(90deg, #1e40af, #7e22ce)',
              border: 'none', borderRadius: 8, color: '#fff',
              fontFamily: 'var(--font-display)', fontWeight: 700,
              fontSize: '0.9rem', letterSpacing: '0.08em', textTransform: 'uppercase',
              cursor: (loading || backendStatus !== 'online') ? 'not-allowed' : 'pointer',
              boxShadow: backendStatus === 'online' ? '0 0 20px rgba(0,212,255,0.3)' : 'none',
              transition: 'all 0.2s',
            }}
          >
            {loading ? '⏳ Analyzing…' : '⚡ Check Prompt'}
          </button>
          <button
            onClick={() => { setPrompt(''); setResult(null); setError(''); }}
            style={{
              padding: '0.7rem 1.2rem', background: 'transparent',
              border: '1px solid var(--border)', borderRadius: 8,
              color: 'var(--text-secondary)', fontFamily: 'var(--font-display)',
              fontWeight: 600, fontSize: '0.85rem', cursor: 'pointer',
            }}
          >
            Clear
          </button>
          <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem', fontFamily: 'var(--font-mono)' }}>
            {prompt.length} chars
          </span>
        </div>
      </div>

      {/* Result */}
      {result && (
        <div className="fade-in" style={{
          ...card,
          border: `1px solid ${result.status === 'blocked' ? 'var(--blocked-color)' : result.status === 'suspicious' ? 'var(--suspicious-color)' : 'var(--allowed-color)'}`,
          boxShadow: `0 0 30px ${result.status === 'blocked' ? 'rgba(255,51,102,0.15)' : result.status === 'suspicious' ? 'rgba(255,214,10,0.1)' : 'rgba(0,255,136,0.1)'}`,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.5rem' }}>
            <div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--text-dim)', letterSpacing: '0.1em', marginBottom: '0.4rem' }}>
                ANALYSIS RESULT &nbsp;
                <span style={{ color: 'var(--neon-green)', fontSize: '0.65rem' }}>[LIVE API]</span>
              </div>
              <StatusBadge status={result.status} large />
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--text-dim)', letterSpacing: '0.1em', marginBottom: '0.2rem' }}>TIMESTAMP</div>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                {new Date(result.timestamp).toLocaleString()}
              </div>
            </div>
          </div>

          <RiskMeter score={result.risk_score} />

          <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'var(--bg-input)', borderRadius: 8, border: '1px solid var(--border)' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--neon-blue)', letterSpacing: '0.1em', marginBottom: '0.4rem' }}>REASON / DETAILS</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>{result.reason}</div>
          </div>

          <div style={{ marginTop: '1rem', padding: '1rem', background: 'var(--bg-input)', borderRadius: 8, border: '1px solid var(--border)' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--text-dim)', letterSpacing: '0.1em', marginBottom: '0.4rem' }}>ANALYZED PROMPT</div>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.6, wordBreak: 'break-word' }}>{result.prompt}</div>
          </div>
        </div>
      )}

      {/* Sample prompts */}
      <div style={card}>
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: 'var(--neon-purple)', letterSpacing: '0.1em', marginBottom: '1rem' }}>
          🧪 SAMPLE TEST PROMPTS
        </div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {SAMPLE_PROMPTS.map((s, i) => (
            <button key={i} onClick={() => loadSample(s)} style={{
              padding: '0.35rem 0.8rem', background: 'var(--bg-input)',
              border: '1px solid var(--border)', borderRadius: 6,
              color: s.category === 'blocked' ? 'var(--blocked-color)' : s.category === 'suspicious' ? 'var(--suspicious-color)' : 'var(--allowed-color)',
              fontFamily: 'var(--font-mono)', fontSize: '0.72rem', cursor: 'pointer', transition: 'border-color 0.2s',
            }}
              onMouseOver={e => e.currentTarget.style.borderColor = 'var(--neon-blue)'}
              onMouseOut={e  => e.currentTarget.style.borderColor = 'var(--border)'}
            >
              {s.label}
            </button>
          ))}
        </div>
        <p style={{ marginTop: '0.8rem', fontFamily: 'var(--font-mono)', fontSize: '0.7rem', color: 'var(--text-dim)' }}>
          ↑ Click a sample to load it, then press Check Prompt.
        </p>
      </div>
    </div>
  );
}
