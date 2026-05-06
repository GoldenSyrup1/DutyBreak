import logging
from vertexai.generative_models import GenerativeModel
from backend.config import VERTEX_MODEL

logger = logging.getLogger(__name__)


CLASSIFIER_PROMPT = """You are an expert trade classification specialist with deep knowledge of the Harmonized System (HS) nomenclature used in international trade.

Given a product description, origin country, and destination country, determine the most accurate 6-digit HS code.

Product Description: {product_description}
Origin Country: {origin_country}
Destination Country: {destination_country}

Respond ONLY with a JSON object in this exact format:
{{
  "hs_code": "XXXXXX",
  "hs_description": "Official HS chapter/heading description",
  "confidence": "HIGH|MEDIUM|LOW",
  "reasoning": "Brief explanation of classification decision"
}}
"""


async def classifier_agent(state: dict) -> dict:
    logger.info(f"ClassifierAgent: classifying '{state['product_description']}'")
    try:
        model = GenerativeModel(VERTEX_MODEL)
        prompt = CLASSIFIER_PROMPT.format(
            product_description=state["product_description"],
            origin_country=state["origin_country"],
            destination_country=state["destination_country"],
        )
        response = await model.generate_content_async(prompt)
        import json, re
        text = response.text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            hs_code = data.get("hs_code", "")
            logger.info(f"ClassifierAgent: HS code → {hs_code}")
            return {**state, "hs_code": hs_code, "tariff_data": {"hs_meta": data}}
    except Exception as e:
        logger.error(f"ClassifierAgent error: {e}")
        return {**state, "errors": state["errors"] + [f"classifier: {str(e)}"]}
    return state
