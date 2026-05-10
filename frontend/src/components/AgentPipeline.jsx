import React from 'react'

const AGENT_DESCRIPTIONS = {
  Classifier: 'HS code classification',
  Tariff: 'Duty rates & trade agreements',
  Compliance: 'Certificates & restrictions',
  Sanctions: 'OFAC / EU / UN screening',
  Document: 'Generating brief',
}

export default function AgentPipeline({ agents, activeAgent, status }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 10,
      padding: 24,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20 }}>
        <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-muted)', letterSpacing: '0.08em' }}>
          AGENT PIPELINE
        </span>
        {status === 'running' && (
          <div style={{ display: 'flex', gap: 3 }}>
            {[0,1,2].map(i => (
              <div key={i} style={{
                width: 4, height: 4, borderRadius: '50%',
                background: 'var(--amber)',
                animation: `pulse-dot 1s ${i * 0.2}s infinite`,
              }} />
            ))}
          </div>
        )}
        {status === 'done' && (
          <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--green)' }}>✓ COMPLETE</span>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        {agents.map((agent, i) => {
          const isDone = i < activeAgent
          const isActive = i === activeAgent && status === 'running'
          const isPending = i > activeAgent

          return (
            <div key={agent} style={{
              display: 'flex',
              alignItems: 'center',
              gap: 14,
              padding: '10px 14px',
              borderRadius: 6,
              background: isActive ? 'rgba(245,158,11,0.06)' : isDone ? 'rgba(16,185,129,0.04)' : 'transparent',
              border: `1px solid ${isActive ? 'rgba(245,158,11,0.3)' : isDone ? 'rgba(16,185,129,0.2)' : 'var(--border)'}`,
              transition: 'all 0.3s',
            }}>
              <div style={{
                width: 20, height: 20,
                borderRadius: '50%',
                border: `2px solid ${isActive ? 'var(--amber)' : isDone ? 'var(--green)' : 'var(--border)'}`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0,
                transition: 'all 0.3s',
              }}>
                {isDone ? (
                  <span style={{ fontSize: 10, color: 'var(--green)' }}>✓</span>
                ) : isActive ? (
                  <div style={{
                    width: 8, height: 8, borderRadius: '50%',
                    background: 'var(--amber)',
                    animation: 'pulse-dot 0.8s infinite',
                  }} />
                ) : (
                  <span style={{ fontFamily: 'var(--mono)', fontSize: 9, color: 'var(--text-dim)' }}>{i+1}</span>
                )}
              </div>

              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{
                    fontFamily: 'var(--mono)',
                    fontSize: 12,
                    fontWeight: 500,
                    color: isActive ? 'var(--amber)' : isDone ? 'var(--text)' : 'var(--text-dim)',
                    letterSpacing: '0.04em',
                  }}>
                    {agent.toUpperCase()} AGENT
                  </span>
                  <span style={{
                    fontFamily: 'var(--mono)',
                    fontSize: 10,
                    color: isActive ? 'var(--amber)' : isDone ? 'var(--green)' : 'var(--text-dim)',
                  }}>
                    {isDone ? 'DONE' : isActive ? 'RUNNING' : 'QUEUED'}
                  </span>
                </div>
                <p style={{
                  fontSize: 12,
                  color: 'var(--text-muted)',
                  marginTop: 2,
                }}>
                  {AGENT_DESCRIPTIONS[agent]}
                </p>
                {isActive && (
                  <div style={{
                    height: 2,
                    background: 'var(--border)',
                    borderRadius: 1,
                    marginTop: 8,
                    overflow: 'hidden',
                  }}>
                    <div style={{
                      height: '100%',
                      background: 'var(--amber)',
                      borderRadius: 1,
                      animation: 'agent-run 1.2s ease-in-out infinite',
                    }} />
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
