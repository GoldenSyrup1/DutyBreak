import logging
import httpx
from vertexai.generative_models import GenerativeModel
from backend.config import VERTEX_MODEL, WTO_API_BASE, COMTRADE_API_KEY

logger = logging.getLogger(__name__)


async def fetch_wto_tariff(hs_code: str, reporter: str, partner: str) -> dict:
    """Fetch MFN tariff rate from WTO API."""
    try:
        url = f"{WTO_API_BASE}/data"
        params = {
            "i": "HS_M_0010",        # MFN applied tariff indicator
            "r": reporter,
            "p": partner,
            "pc": hs_code[:6],
            "fmt": "json",
            "max": 1,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        logger.warning(f"WTO API fetch failed: {e}")
    return {}


TARIFF_PROMPT = """You are an international trade tariff expert.

Given the following information, provide a detailed tariff analysis:

HS Code: {hs_code}
Origin Country: {origin_country} 
Destination Country: {destination_country}
WTO Data: {wto_data}

Respond ONLY with a JSON object:
{{
  "mfn_rate": "X.X%",
  "preferential_rate": "X.X% or null",
  "trade_agreement": "Agreement name or null",
  "estimated_duty_usd": null,
  "notes": "Any important tariff notes",
  "rules_of_origin": "Key rules of origin requirements if preferential rate applies"
}}
"""


async def tariff_agent(state: dict) -> dict:
    logger.info(f"TariffAgent: looking up tariffs for HS {state['hs_code']}")
    try:
        wto_data = await fetch_wto_tariff(
            state["hs_code"],
            state["destination_country"],
            state["origin_country"],
        )
        model = GenerativeModel(VERTEX_MODEL)
        prompt = TARIFF_PROMPT.format(
            hs_code=state["hs_code"],
            origin_country=state["origin_country"],
            destination_country=state["destination_country"],
            wto_data=str(wto_data),
        )
        response = await model.generate_content_async(prompt)
        import json, re
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            existing = state.get("tariff_data", {})
            return {**state, "tariff_data": {**existing, **data}}
    except Exception as e:
        logger.error(f"TariffAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"tariff: {str(e)}"]}
    return state
