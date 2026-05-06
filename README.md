# DutyBreak

**Global trade, cleared in 90 seconds.**

DutyBreak is an agentic trade compliance co-pilot that removes the biggest barrier to global trade for small and medium businesses. Input a product, an origin country, and a destination country — five AI agents do the rest.

Built for the **Google Cloud Rapid Agent Hackathon 2026**.

---

## The Problem

500 million SMEs globally want to trade across borders. Large corporations have compliance teams, trade lawyers, and intelligence desks. SMEs have nothing. A single missed certificate, wrong HS code, or unscreened sanctioned supplier can result in seized shipments, fines, or criminal liability.

DutyBreak democratises access to world-class trade compliance intelligence.

---

## Agent Architecture

Five LangGraph agents run sequentially on a shared state:

```
Input: product + origin + destination
        ↓
[1] ClassifierAgent   → HS code (6-digit Harmonized System)
        ↓
[2] TariffAgent       → MFN/preferential rates, trade agreements, duty calc
        ↓
[3] ComplianceAgent   → certificates, licenses, labeling laws, restrictions
        ↓
[4] SanctionsAgent    → OFAC / EU / UN sanctions screening
        ↓
[5] DocumentAgent     → full compliance brief + action items
        ↓
Output: structured compliance package
```

---

## Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM | Vertex AI (Gemini 1.5 Pro) |
| Backend | FastAPI |
| Vector Store | Qdrant |
| Deployment | Google Cloud Run |
| Frontend | React + Vite |
| Data Sources | WTO, UN Comtrade, EU TARIC, US HTS, OFAC SDN |

---

## Getting Started

### 1. Clone & setup
```bash
git clone git@github.com:GoldenSyrup1/DutyBreak.git
cd DutyBreak
```

### 2. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
# Fill in .env with your GCP project ID
```

### 3. Authenticate with Google Cloud
```bash
gcloud auth application-default login
```

### 4. Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 5. Run backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 6. Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## API

### POST `/api/compliance/check`
```json
{
  "product_description": "Lithium-ion battery packs for electric bicycles",
  "origin_country": "CN",
  "destination_country": "DE",
  "supplier_name": "Shenzhen PowerCell Ltd"
}
```

Returns a full compliance brief including HS code, tariff rates, required certificates, sanctions status, and prioritised action items.

---

## Demo Scenario

> A manufacturer in Vietnam wants to export ceramic kitchenware to Germany.

1. DutyBreak classifies the product as HS 6911.10
2. Identifies 12% EU MFN duty rate, reduced to 0% under EVFTA
3. Flags CE marking and REACH compliance requirements
4. Screens against all three major sanctions lists — clear
5. Generates a 5-step action plan with estimated 7-day clearance

**Time to brief: ~90 seconds.**
