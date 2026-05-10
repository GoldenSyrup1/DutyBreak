import json, re, logging, httpx
from backend.services.gemini import generate
from backend.config import WTO_API_BASE
logger = logging.getLogger(__name__)

async def fetch_wto_tariff(hs_code, reporter, partner):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{WTO_API_BASE}/data", params={"i":"HS_M_0010","r":reporter,"p":partner,"pc":hs_code[:6],"fmt":"json","max":1})
            if resp.status_code == 200: return resp.json()
    except: pass
    return {}

TARIFF_PROMPT = """You are an international trade tariff expert.
HS Code: {hs_code}, Origin: {origin_country}, Destination: {destination_country}, WTO Data: {wto_data}
Respond ONLY with JSON: {{"mfn_rate":"X%","preferential_rate":"X% or null","trade_agreement":"name or null","estimated_duty_usd":null,"notes":"notes","rules_of_origin":"rules"}}"""

async def tariff_agent(state: dict) -> dict:
    logger.info(f"TariffAgent: looking up tariffs for HS {state['hs_code']}")
    try:
        wto = await fetch_wto_tariff(state["hs_code"], state["destination_country"], state["origin_country"])
        text = await generate(TARIFF_PROMPT.format(hs_code=state["hs_code"], origin_country=state["origin_country"], destination_country=state["destination_country"], wto_data=str(wto)))
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            return {**state, "tariff_data": {**state.get("tariff_data",{}), **json.loads(m.group())}}
    except Exception as e:
        logger.error(f"TariffAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"tariff: {str(e)}"]}
    return state
