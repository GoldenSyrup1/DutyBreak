import json, re, logging
from backend.services.gemini import generate
logger = logging.getLogger(__name__)

COMPLIANCE_PROMPT = """You are an expert in international trade compliance and customs regulations.
Product: {product_description}, HS Code: {hs_code}, Origin: {origin_country}, Destination: {destination_country}
Respond ONLY with JSON: {{"required_certificates":[],"import_licenses":[],"labeling_requirements":[],"import_restrictions":[],"customs_procedures":"description","estimated_processing_days":5,"regulatory_bodies":[]}}"""

async def compliance_agent(state: dict) -> dict:
    logger.info(f"ComplianceAgent: mapping requirements for HS {state['hs_code']}")
    try:
        text = await generate(COMPLIANCE_PROMPT.format(product_description=state["product_description"], hs_code=state["hs_code"], origin_country=state["origin_country"], destination_country=state["destination_country"]))
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m: return {**state, "compliance_data": json.loads(m.group())}
    except Exception as e:
        logger.error(f"ComplianceAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"compliance: {str(e)}"]}
    return state
