import logging
from vertexai.generative_models import GenerativeModel
from backend.config import VERTEX_MODEL

logger = logging.getLogger(__name__)


DOCUMENT_PROMPT = """You are a senior trade compliance officer writing an executive compliance brief.

Synthesize all findings into a clear, actionable compliance brief.

Product: {product_description}
HS Code: {hs_code}
Route: {origin_country} → {destination_country}
Tariff Data: {tariff_data}
Compliance Data: {compliance_data}
Sanctions Data: {sanctions_data}

Respond ONLY with a JSON object:
{{
  "summary": "2-3 sentence executive summary of this trade's compliance status",
  "overall_risk": "LOW|MEDIUM|HIGH|BLOCKED",
  "action_items": [
    "1. Obtain Certificate of Origin from ...",
    "2. Declare HS code 1234.56 on customs entry form",
    "..."
  ],
  "estimated_total_cost_impact": "X% of shipment value in duties and fees",
  "estimated_clearance_days": 5,
  "next_steps": "What the exporter should do first"
}}
"""


async def document_agent(state: dict) -> dict:
    logger.info("DocumentAgent: generating compliance brief")
    try:
        model = GenerativeModel(VERTEX_MODEL)
        prompt = DOCUMENT_PROMPT.format(
            product_description=state["product_description"],
            hs_code=state["hs_code"],
            origin_country=state["origin_country"],
            destination_country=state["destination_country"],
            tariff_data=state.get("tariff_data", {}),
            compliance_data=state.get("compliance_data", {}),
            sanctions_data=state.get("sanctions_data", {}),
        )
        response = await model.generate_content_async(prompt)
        import json, re
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            brief = {
                "product_description": state["product_description"],
                "hs_code": state["hs_code"],
                "origin_country": state["origin_country"],
                "destination_country": state["destination_country"],
                "tariff": state.get("tariff_data", {}),
                "compliance": state.get("compliance_data", {}),
                "sanctions": state.get("sanctions_data", {}),
                **data,
            }
            logger.info(f"DocumentAgent: brief generated, risk={data.get('overall_risk')}")
            return {**state, "compliance_brief": brief}
    except Exception as e:
        logger.error(f"DocumentAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"document: {str(e)}"]}
    return state
