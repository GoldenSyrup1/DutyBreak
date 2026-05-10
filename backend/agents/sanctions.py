import json, re, logging
from backend.services.gemini import generate
logger = logging.getLogger(__name__)
OFAC_HIGH_RISK = {"IR","KP","CU","SY","RU","BY"}
EU_RESTRICTED = {"IR","KP","SY","RU","BY","MM"}
UN_RESTRICTED = {"IR","KP","ML","CF","YE","LY","SO"}

SANCTIONS_PROMPT = """You are a sanctions and trade compliance expert.
Product: {product_description}, HS: {hs_code}, Origin: {origin_country}, Destination: {destination_country}, Supplier: {supplier_name}, Flags: {flags}
Respond ONLY with JSON: {{"is_sanctioned":false,"risk_level":"LOW|MEDIUM|HIGH|BLOCKED","flags":[],"screened_lists":["OFAC SDN","EU Consolidated","UN Security Council"],"recommended_action":"PROCEED|ENHANCED_DUE_DILIGENCE|BLOCK","notes":"notes"}}"""

async def sanctions_agent(state: dict) -> dict:
    logger.info(f"SanctionsAgent: screening {state['origin_country']} -> {state['destination_country']}")
    flags = []
    o, d = state["origin_country"].upper(), state["destination_country"].upper()
    if o in OFAC_HIGH_RISK or d in OFAC_HIGH_RISK: flags.append("OFAC high-risk country")
    if o in EU_RESTRICTED or d in EU_RESTRICTED: flags.append("EU restricted country")
    if o in UN_RESTRICTED or d in UN_RESTRICTED: flags.append("UN measures apply")
    try:
        text = await generate(SANCTIONS_PROMPT.format(product_description=state["product_description"], hs_code=state["hs_code"], origin_country=state["origin_country"], destination_country=state["destination_country"], supplier_name=state.get("supplier_name") or "Not provided", flags=flags))
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m: return {**state, "sanctions_data": json.loads(m.group())}
    except Exception as e:
        logger.error(f"SanctionsAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"sanctions: {str(e)}"]}
    return state
