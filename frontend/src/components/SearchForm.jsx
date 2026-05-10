import React, { useState } from 'react'

const COUNTRIES = [
  { code: 'AU', name: 'Australia' }, { code: 'BR', name: 'Brazil' },
  { code: 'CN', name: 'China' }, { code: 'DE', name: 'Germany' },
  { code: 'FR', name: 'France' }, { code: 'GB', name: 'United Kingdom' },
  { code: 'ID', name: 'Indonesia' }, { code: 'IN', name: 'India' },
  { code: 'IR', name: 'Iran' }, { code: 'JP', name: 'Japan' },
  { code: 'KE', name: 'Kenya' }, { code: 'KP', name: 'North Korea' },
  { code: 'MX', name: 'Mexico' }, { code: 'MY', name: 'Malaysia' },
  { code: 'NG', name: 'Nigeria' }, { code: 'NL', name: 'Netherlands' },
  { code: 'PH', name: 'Philippines' }, { code: 'RU', name: 'Russia' },
  { code: 'SG', name: 'Singapore' }, { code: 'TH', name: 'Thailand' },
  { code: 'US', name: 'United States' }, { code: 'VN', name: 'Vietnam' },
  { code: 'ZA', name: 'South Africa' },
]

const inputStyle = {
  width: '100%',
  background: 'var(--surface)',
  border: '1px solid var(--border)',
  borderRadius: 6,
  padding: '10px 14px',
  color: 'var(--text)',
  fontFamily: 'var(--sans)',
  fontSize: 14,
  outline: 'none',
  transition: 'border-color 0.2s',
}

const labelStyle = {
  display: 'block',
  fontFamily: 'var(--mono)',
  fontSize: 11,
  color: 'var(--text-muted)',
  letterSpacing: '0.08em',
  marginBottom: 6,
}

export default function SearchForm({ onSubmit, disabled }) {
  const [form, setForm] = useState({
    product_description: '',
    origin_country: 'CN',
    destination_country: 'DE',
    supplier_name: '',
  })
  const [focused, setFocused] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.product_description.trim()) return
    onSubmit(form)
  }

  const field = (name) => ({
    value: form[name],
    onChange: e => setForm(p => ({ ...p, [name]: e.target.value })),
    onFocus: () => setFocused(name),
    onBlur: () => setFocused(null),
    style: { ...inputStyle, borderColor: focused === name ? 'var(--amber)' : 'var(--border)' },
  })

  return (
    <div>
      <div style={{ marginBottom: 32 }}>
        <h1 style={{ fontFamily: 'var(--mono)', fontSize: 24, fontWeight: 600, letterSpacing: '-0.02em' }}>
          TRADE <span style={{ color: 'var(--amber)' }}>COMPLIANCE</span> INTEL
        </h1>
        <p style={{ marginTop: 8, color: 'var(--text-muted)', fontSize: 14, maxWidth: 480 }}>
          5 agents. 1 compliance brief. Global trade, cleared in 90 seconds.
        </p>
      </div>

      <form onSubmit={handleSubmit} style={{
        background: 'var(--surface)',
        border: '1px solid var(--border)',
        borderRadius: 10,
        padding: 24,
      }}>
        <div style={{ marginBottom: 20 }}>
          <label style={labelStyle}>PRODUCT DESCRIPTION *</label>
          <textarea
            placeholder="e.g. Lithium-ion battery packs for electric bicycles"
            rows={3}
            {...field('product_description')}
            style={{ ...field('product_description').style, resize: 'vertical', lineHeight: 1.5 }}
            required
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
          <div>
            <label style={labelStyle}>ORIGIN COUNTRY *</label>
            <select {...field('origin_country')} style={{ ...field('origin_country').style, cursor: 'pointer' }}>
              {COUNTRIES.map(c => (
                <option key={c.code} value={c.code}>{c.name} ({c.code})</option>
              ))}
            </select>
          </div>
          <div>
            <label style={labelStyle}>DESTINATION COUNTRY *</label>
            <select {...field('destination_country')} style={{ ...field('destination_country').style, cursor: 'pointer' }}>
              {COUNTRIES.map(c => (
                <option key={c.code} value={c.code}>{c.name} ({c.code})</option>
              ))}
            </select>
          </div>
        </div>

        <div style={{ marginBottom: 24 }}>
          <label style={labelStyle}>SUPPLIER NAME <span style={{ color: 'var(--text-dim)' }}>(OPTIONAL)</span></label>
          <input
            type="text"
            placeholder="e.g. Shenzhen PowerCell Ltd"
            {...field('supplier_name')}
          />
        </div>

        <button
          type="submit"
          disabled={disabled || !form.product_description.trim()}
          style={{
            width: '100%',
            padding: '12px 24px',
            background: disabled ? 'var(--surface-2)' : 'var(--amber)',
            color: disabled ? 'var(--text-muted)' : '#000',
            border: 'none',
            borderRadius: 6,
            fontFamily: 'var(--mono)',
            fontSize: 13,
            fontWeight: 600,
            letterSpacing: '0.08em',
            cursor: disabled ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s',
          }}
        >
          {disabled ? 'RUNNING AGENTS...' : 'RUN COMPLIANCE CHECK →'}
        </button>
      </form>
    </div>
  )
}
