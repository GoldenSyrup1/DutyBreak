import logging
import vertexai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.config import GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
from backend.models.schemas import ComplianceRequest
from backend.graph.workflow import run_compliance_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_LOCATION)

app = FastAPI(
    title="DutyBreak API",
    description="Agentic trade compliance co-pilot — global trade, cleared in 90 seconds.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "DutyBreak"}


@app.post("/api/compliance/check")
async def compliance_check(req: ComplianceRequest):
    """
    Run the full 5-agent compliance pipeline.
    Returns a structured compliance brief in ~90 seconds.
    """
    logger.info(f"Compliance check: {req.product_description} | {req.origin_country} → {req.destination_country}")
    try:
        result = await run_compliance_check(
            product_description=req.product_description,
            origin_country=req.origin_country,
            destination_country=req.destination_country,
            supplier_name=req.supplier_name,
        )
        if result.get("errors"):
            logger.warning(f"Pipeline completed with errors: {result['errors']}")
        return {
            "success": True,
            "brief": result.get("compliance_brief", {}),
            "errors": result.get("errors", []),
        }
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/countries")
async def list_countries():
    """Return supported ISO country codes."""
    return {
        "countries": [
            {"code": "AU", "name": "Australia"},
            {"code": "CN", "name": "China"},
            {"code": "DE", "name": "Germany"},
            {"code": "GB", "name": "United Kingdom"},
            {"code": "IN", "name": "India"},
            {"code": "JP", "name": "Japan"},
            {"code": "SG", "name": "Singapore"},
            {"code": "US", "name": "United States"},
            {"code": "VN", "name": "Vietnam"},
            {"code": "ID", "name": "Indonesia"},
            {"code": "MY", "name": "Malaysia"},
            {"code": "TH", "name": "Thailand"},
            {"code": "PH", "name": "Philippines"},
            {"code": "BR", "name": "Brazil"},
            {"code": "MX", "name": "Mexico"},
            {"code": "ZA", "name": "South Africa"},
            {"code": "NG", "name": "Nigeria"},
            {"code": "KE", "name": "Kenya"},
            {"code": "FR", "name": "France"},
            {"code": "NL", "name": "Netherlands"},
        ]
    }
