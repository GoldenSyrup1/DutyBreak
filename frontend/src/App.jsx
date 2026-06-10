import React, { useState } from 'react'
import SearchForm from './components/SearchForm'
import AgentPipeline from './components/AgentPipeline'
import ComplianceBrief from './components/ComplianceBrief'

const AGENTS = ['Classifier', 'Tariff', 'Compliance', 'Sanctions', 'Document']

export default function App() {
  const [status, setStatus] = useState('idle') // idle | running | done | error
  const [activeAgent, setActiveAgent] = useState(-1)
  const [result, setResult] = useState(null)

  const handleSubmit = async (formData) => {
    setStatus('running')
    setResult(null)
    setActiveAgent(0)

    // Simulate agent progression while waiting for response
    const interval = setInterval(() => {
      setActiveAgent(prev => {
        if (prev < AGENTS.length - 1) return prev + 1
        clearInterval(interval)
        return prev
      })
    }, 1200)

    try {
      const res = await fetch('https://dutybreak-371750677349.us-central1.run.app/api/compliance/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      const data = await res.json()
      clearInterval(interval)
      setActiveAgent(AGENTS.length)
      setResult(data)
      setStatus(data.brief && Object.keys(data.brief).length > 0 ? 'done' : 'error')
    } catch (err) {
      clearInterval(interval)
      setStatus('error')
      setResult({ errors: [String(err)] })
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <main style={{ flex: 1, maxWidth: 960, margin: '0 auto', padding: '40px 24px', width: '100%' }}>
        <SearchForm onSubmit={handleSubmit} disabled={status === 'running'} />
        {status !== 'idle' && (
          <div style={{ marginTop: 40 }}>
            <AgentPipeline agents={AGENTS} activeAgent={activeAgent} status={status} />
          </div>
        )}
        {status === 'done' && result?.brief && (
          <div style={{ marginTop: 40 }} className="fade-up">
            <ComplianceBrief brief={result.brief} />
          </div>
        )}
        {status === 'error' && (
          <div style={{ marginTop: 32, padding: '20px 24px', background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 8 }}>
            <p style={{ fontFamily: 'var(--mono)', fontSize: 13, color: 'var(--red)' }}>
              Pipeline error — check API quota or try again.
            </p>
            {result?.errors?.[0] && (
              <p style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-muted)', marginTop: 8, wordBreak: 'break-all' }}>
                {result.errors[0].slice(0, 200)}...
              </p>
            )}
          </div>
        )}
      </main>
      <Footer />
    </div>
  )
}

function Header() {
  return (
    <header style={{
      borderBottom: '1px solid var(--border)',
      padding: '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      height: 56,
      background: 'rgba(8,12,20,0.95)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{
          width: 28, height: 28, borderRadius: 6,
          background: 'linear-gradient(135deg, var(--amber) 0%, #D97706 100%)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 14, fontWeight: 700, color: '#000',
          fontFamily: 'var(--mono)',
        }}>D</div>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 14, fontWeight: 600, letterSpacing: '0.05em' }}>
          DUTY<span style={{ color: 'var(--amber)' }}>BREAK</span>
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <div style={{ width: 6, height: 6, borderRadius: '50%', background: 'var(--green)', animation: 'pulse-dot 2s infinite' }} />
        <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-muted)' }}>SYSTEM ONLINE</span>
      </div>
    </header>
  )
}

function Footer() {
  return (
    <footer style={{ borderTop: '1px solid var(--border)', padding: '16px 24px', textAlign: 'center' }}>
      <p style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-dim)' }}>
        DUTYBREAK v1.0 — 5-AGENT TRADE COMPLIANCE PIPELINE — GOOGLE CLOUD RAPID AGENT HACKATHON 2026
      </p>
    </footer>
  )
}
