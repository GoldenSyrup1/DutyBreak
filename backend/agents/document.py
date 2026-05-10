import json, re, logging
from backend.services.gemini import generate
logger = logging.getLogger(__name__)

DOCUMENT_PROMPT = """You are a senior trade compliance officer.
Product: {product_description}, HS: {hs_code}, Route: {origin_country} -> {destination_country}
Tariff: {tariff_data}, Compliance: {compliance_data}, Sanctions: {sanctions_data}
Respond ONLY with JSON: {{"summary":"2-3 sentence summary","overall_risk":"LOW|MEDIUM|HIGH|BLOCKED","action_items":["1. ...","2. ..."],"estimated_total_cost_impact":"X%","estimated_clearance_days":5,"next_steps":"first action"}}"""

async def document_agent(state: dict) -> dict:
    logger.info("DocumentAgent: generating compliance brief")
    try:
        text = await generate(DOCUMENT_PROMPT.format(product_description=state["product_description"], hs_code=state["hs_code"], origin_country=state["origin_country"], destination_country=state["destination_country"], tariff_data=state.get("tariff_data",{}), compliance_data=state.get("compliance_data",{}), sanctions_data=state.get("sanctions_data",{})))
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            data = json.loads(m.group())
            brief = {"product_description": state["product_description"], "hs_code": state["hs_code"], "origin_country": state["origin_country"], "destination_country": state["destination_country"], "tariff": state.get("tariff_data",{}), "compliance": state.get("compliance_data",{}), "sanctions": state.get("sanctions_data",{}), **data}
            logger.info(f"DocumentAgent: risk={data.get('overall_risk')}")
            return {**state, "compliance_brief": brief}
    except Exception as e:
        logger.error(f"DocumentAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"document: {str(e)}"]}
    return state
