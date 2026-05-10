import json, re, logging
from backend.services.gemini import generate
logger = logging.getLogger(__name__)

CLASSIFIER_PROMPT = """You are an expert trade classification specialist with deep knowledge of the Harmonized System (HS) nomenclature.
Product Description: {product_description}
Origin Country: {origin_country}
Destination Country: {destination_country}
Respond ONLY with a JSON object:
{{"hs_code": "XXXXXX","hs_description": "Official HS description","confidence": "HIGH|MEDIUM|LOW","reasoning": "Brief explanation"}}"""

async def classifier_agent(state: dict) -> dict:
    logger.info(f"ClassifierAgent: classifying '{state['product_description']}'")
    try:
        text = await generate(CLASSIFIER_PROMPT.format(**{k: state[k] for k in ["product_description","origin_country","destination_country"]}))
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            data = json.loads(m.group())
            logger.info(f"ClassifierAgent: HS code -> {data.get('hs_code')}")
            return {**state, "hs_code": data.get("hs_code",""), "tariff_data": {"hs_meta": data}}
    except Exception as e:
        logger.error(f"ClassifierAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"classifier: {str(e)}"]}
    return state
