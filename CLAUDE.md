# DutyBreak — Project Memory

## What is DutyBreak?
An agentic trade compliance co-pilot that takes a product, an origin country, and a destination country — and handles everything else. It classifies HS tariff codes, maps applicable duties and regulations, screens against sanctions lists, identifies required certificates, and generates a full compliance brief. Built for the Google Cloud Rapid Agent Hackathon 2026.

**Tagline:** Global trade, cleared in 90 seconds.

## Stack
- **Backend:** FastAPI (Python)
- **Agent Orchestration:** LangGraph
- **LLM:** Vertex AI (Gemini 1.5 Pro)
- **Vector Store:** Qdrant (regulation embeddings)
- **Deployment:** Google Cloud Run
- **Frontend:** React + Vite
- **Data:** UN Comtrade, WTO Tariff DB, EU TARIC, US HTS, OFAC SDN

## Repo
`git@github.com:GoldenSyrup1/DutyBreak.git`

## Root (local)
- Windows: `C:\Users\srira\OneDrive\Documents\STARTUPS\DutyBreak`
- WSL: `/mnt/c/Users/srira/OneDrive/Documents/STARTUPS/DutyBreak`

## Agent Architecture
Five LangGraph agents run sequentially with shared state:

1. **ClassifierAgent** — Takes product description → HS code (6-digit Harmonized System)
2. **TariffAgent** — HS code + origin + destination → tariff rates, trade agreements, duty calculations
3. **ComplianceAgent** — Maps required certificates, licenses, labeling laws, import restrictions
4. **SanctionsAgent** — Screens origin country, supplier, and product against OFAC/EU/UN sanctions
5. **DocumentAgent** — Synthesizes all above into a structured compliance brief (JSON + PDF-ready)

## LangGraph State Shape
```python
class DutyBreakState(TypedDict):
    product_description: str
    origin_country: str        # ISO 3166-1 alpha-2
    destination_country: str   # ISO 3166-1 alpha-2
    hs_code: str
    tariff_data: dict
    compliance_data: dict
    sanctions_data: dict
    compliance_brief: dict
    errors: list[str]
```

## Key Data Sources
- **UN Comtrade API** — trade flow data
- **WTO Tariff Download Facility** — MFN and preferential tariff rates
- **EU TARIC** — EU-specific tariff + regulation database
- **US HTS (USITC)** — US Harmonized Tariff Schedule
- **OFAC SDN List** — US sanctions
- **EU Consolidated Sanctions List**
- **UN Security Council Sanctions**

## Services (local dev)
- Qdrant: `http://localhost:6333`
- FastAPI: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## Environment Variables
See `.env.example`

## Future Integration
- WEPort: ClearPath compliance check before freight booking
- StockUp: tariff shock → market signal correlation
- TrackLink: sector exposure mapping

## Dev Notes
- Prefer manual service startup
- Keep agents modular — each agent is independently testable
- All agent tools are in `backend/tools/`, imported by agents
- LangGraph workflow defined in `backend/graph/workflow.py`
