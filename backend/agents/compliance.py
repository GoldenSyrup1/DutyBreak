import logging
from vertexai.generative_models import GenerativeModel
from backend.config import VERTEX_MODEL

logger = logging.getLogger(__name__)


COMPLIANCE_PROMPT = """You are an expert in international trade compliance, customs regulations, and import/export law.

Determine all compliance requirements for this trade:

Product: {product_description}
HS Code: {hs_code}
Origin: {origin_country}
Destination: {destination_country}

Respond ONLY with a JSON object:
{{
  "required_certificates": ["Certificate of Origin", "..."],
  "import_licenses": ["list or empty"],
  "labeling_requirements": ["list of labeling laws that apply"],
  "import_restrictions": ["any bans, quotas, or special controls"],
  "customs_procedures": "Brief description of customs entry procedure",
  "estimated_processing_days": 5,
  "regulatory_bodies": ["list of agencies that govern this import"]
}}
"""


async def compliance_agent(state: dict) -> dict:
    logger.info(f"ComplianceAgent: mapping requirements for HS {state['hs_code']}")
    try:
        model = GenerativeModel(VERTEX_MODEL)
        prompt = COMPLIANCE_PROMPT.format(
            product_description=state["product_description"],
            hs_code=state["hs_code"],
            origin_country=state["origin_country"],
            destination_country=state["destination_country"],
        )
        response = await model.generate_content_async(prompt)
        import json, re
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {**state, "compliance_data": data}
    except Exception as e:
        logger.error(f"ComplianceAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"compliance: {str(e)}"]}
    return state
