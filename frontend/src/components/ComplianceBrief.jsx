import React from 'react'

const riskColors = {
  LOW: 'var(--green)',
  MEDIUM: 'var(--amber)',
  HIGH: '#F97316',
  BLOCKED: 'var(--red)',
}

const riskBg = {
  LOW: 'rgba(16,185,129,0.08)',
  MEDIUM: 'rgba(245,158,11,0.08)',
  HIGH: 'rgba(249,115,22,0.08)',
  BLOCKED: 'rgba(239,68,68,0.08)',
}

function Section({ title, children }) {
  return (
    <div style={{
      background: 'var(--surface)',
      border: '1px solid var(--border)',
      borderRadius: 8,
      padding: 20,
    }}>
      <p style={{
        fontFamily: 'var(--mono)',
        fontSize: 10,
        color: 'var(--text-muted)',
        letterSpacing: '0.1em',
        marginBottom: 14,
      }}>{title}</p>
      {children}
    </div>
  )
}

function DataRow({ label, value, mono = false, highlight = false }) {
  return (
    <div style={{
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'flex-start',
      gap: 16,
      padding: '8px 0',
      borderBottom: '1px solid var(--border)',
    }}>
      <span style={{ fontSize: 12, color: 'var(--text-muted)', flexShrink: 0 }}>{label}</span>
      <span style={{
        fontFamily: mono ? 'var(--mono)' : 'var(--sans)',
        fontSize: 13,
        color: highlight ? 'var(--amber)' : 'var(--text)',
        textAlign: 'right',
        fontWeight: mono ? 500 : 400,
      }}>{value || '—'}</span>
    </div>
  )
}

export default function ComplianceBrief({ brief }) {
  const risk = brief.overall_risk || 'LOW'
  const tariff = brief.tariff || {}
  const compliance = brief.compliance || {}
  const sanctions = brief.sanctions || {}

  return (
    <div>
      {/* Header */}
      <div style={{
        background: riskBg[risk] || 'var(--surface)',
        border: `1px solid ${riskColors[risk] || 'var(--border)'}`,
        borderRadius: 10,
        padding: '20px 24px',
        marginBottom: 20,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        gap: 16,
      }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 10 }}>
            <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-muted)', letterSpacing: '0.1em' }}>
              COMPLIANCE BRIEF
            </span>
            <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-dim)' }}>
              {brief.origin_country} → {brief.destination_country}
            </span>
          </div>
          <p style={{ fontSize: 14, color: 'var(--text)', lineHeight: 1.6 }}>
            {brief.summary}
          </p>
        </div>
        <div style={{ flexShrink: 0, textAlign: 'right' }}>
          <div style={{
            fontFamily: 'var(--mono)',
            fontSize: 20,
            fontWeight: 600,
            color: riskColors[risk],
            letterSpacing: '0.05em',
          }}>{risk}</div>
          <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-dim)', marginTop: 2 }}>
            RISK LEVEL
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
        {/* Classification */}
        <Section title="CLASSIFICATION">
          <DataRow label="HS Code" value={brief.hs_code} mono highlight />
          <DataRow label="Product" value={brief.product_description?.slice(0, 50) + (brief.product_description?.length > 50 ? '...' : '')} />
          <DataRow label="Clearance Est." value={`${brief.estimated_clearance_days || '—'} days`} mono />
          <DataRow label="Cost Impact" value={brief.estimated_total_cost_impact} />
        </Section>

        {/* Tariff */}
        <Section title="TARIFF INTELLIGENCE">
          <DataRow label="MFN Rate" value={tariff.mfn_rate} mono highlight />
          <DataRow label="Preferential Rate" value={tariff.preferential_rate} mono />
          <DataRow label="Trade Agreement" value={tariff.trade_agreement} />
          <DataRow label="Rules of Origin" value={tariff.rules_of_origin?.slice(0, 60)} />
        </Section>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
        {/* Sanctions */}
        <Section title="SANCTIONS SCREENING">
          <DataRow
            label="Risk Level"
            value={sanctions.risk_level}
            mono
            highlight={sanctions.risk_level !== 'LOW'}
          />
          <DataRow label="Recommendation" value={sanctions.recommended_action} mono />
          <DataRow label="Lists Screened" value={sanctions.screened_lists?.join(', ')} />
          {sanctions.flags?.length > 0 && (
            <div style={{ marginTop: 8 }}>
              {sanctions.flags.map((f, i) => (
                <div key={i} style={{
                  fontFamily: 'var(--mono)',
                  fontSize: 11,
                  color: 'var(--red)',
                  padding: '4px 0',
                }}>⚠ {f}</div>
              ))}
            </div>
          )}
        </Section>

        {/* Compliance */}
        <Section title="COMPLIANCE REQUIREMENTS">
          {compliance.required_certificates?.length > 0 && (
            <div style={{ marginBottom: 10 }}>
              <p style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 6 }}>Certificates Required</p>
              {compliance.required_certificates.slice(0, 4).map((c, i) => (
                <div key={i} style={{
                  fontSize: 12, color: 'var(--text)',
                  padding: '3px 0',
                  borderBottom: '1px solid var(--border)',
                }}>• {c}</div>
              ))}
            </div>
          )}
          <DataRow label="Processing Days" value={`~${compliance.estimated_processing_days || '—'} days`} mono />
        </Section>
      </div>

      {/* Action Items */}
      {brief.action_items?.length > 0 && (
        <Section title="ACTION ITEMS">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {brief.action_items.map((item, i) => (
              <div key={i} style={{
                display: 'flex',
                gap: 12,
                padding: '10px 14px',
                background: 'var(--surface-2)',
                borderRadius: 6,
                border: '1px solid var(--border)',
              }}>
                <span style={{
                  fontFamily: 'var(--mono)',
                  fontSize: 11,
                  color: 'var(--amber)',
                  flexShrink: 0,
                  marginTop: 1,
                }}>{String(i+1).padStart(2,'0')}</span>
                <span style={{ fontSize: 13, color: 'var(--text)', lineHeight: 1.5 }}>{item}</span>
              </div>
            ))}
          </div>
          {brief.next_steps && (
            <div style={{
              marginTop: 12,
              padding: '12px 14px',
              background: 'rgba(245,158,11,0.06)',
              borderRadius: 6,
              border: '1px solid rgba(245,158,11,0.2)',
            }}>
              <p style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--amber)', marginBottom: 4 }}>NEXT STEP</p>
              <p style={{ fontSize: 13, color: 'var(--text)' }}>{brief.next_steps}</p>
            </div>
          )}
        </Section>
      )}
    </div>
  )
}
