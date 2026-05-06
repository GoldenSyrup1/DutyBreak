import logging
import httpx
from vertexai.generative_models import GenerativeModel
from backend.config import VERTEX_MODEL

logger = logging.getLogger(__name__)

# High-risk country lists (simplified — expand with live API in production)
OFAC_HIGH_RISK = {"IR", "KP", "CU", "SY", "RU", "BY"}
EU_RESTRICTED = {"IR", "KP", "SY", "RU", "BY", "MM"}
UN_RESTRICTED = {"IR", "KP", "ML", "CF", "YE", "LY", "SO"}

SANCTIONS_PROMPT = """You are a sanctions and trade compliance expert.

Assess the sanctions risk for this trade:

Product: {product_description}
HS Code: {hs_code}
Origin Country: {origin_country}
Destination Country: {destination_country}
Supplier: {supplier_name}
Flags detected: {flags}

Respond ONLY with a JSON object:
{{
  "is_sanctioned": false,
  "risk_level": "LOW|MEDIUM|HIGH|BLOCKED",
  "flags": ["list any specific risk flags"],
  "screened_lists": ["OFAC SDN", "EU Consolidated", "UN Security Council"],
  "recommended_action": "PROCEED|ENHANCED_DUE_DILIGENCE|BLOCK",
  "notes": "Any important sanctions notes"
}}
"""


async def sanctions_agent(state: dict) -> dict:
    logger.info(f"SanctionsAgent: screening {state['origin_country']} → {state['destination_country']}")
    flags = []
    
    origin = state["origin_country"].upper()
    dest = state["destination_country"].upper()

    if origin in OFAC_HIGH_RISK or dest in OFAC_HIGH_RISK:
        flags.append(f"OFAC high-risk country: {origin if origin in OFAC_HIGH_RISK else dest}")
    if origin in EU_RESTRICTED or dest in EU_RESTRICTED:
        flags.append(f"EU restricted country detected")
    if origin in UN_RESTRICTED or dest in UN_RESTRICTED:
        flags.append(f"UN Security Council measures apply")

    try:
        model = GenerativeModel(VERTEX_MODEL)
        prompt = SANCTIONS_PROMPT.format(
            product_description=state["product_description"],
            hs_code=state["hs_code"],
            origin_country=state["origin_country"],
            destination_country=state["destination_country"],
            supplier_name=state.get("supplier_name") or "Not provided",
            flags=flags,
        )
        response = await model.generate_content_async(prompt)
        import json, re
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return {**state, "sanctions_data": data}
    except Exception as e:
        logger.error(f"SanctionsAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"sanctions: {str(e)}"]}
    return state
