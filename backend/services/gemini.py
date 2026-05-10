import httpx
from backend.config import GEMINI_API_KEY, VERTEX_MODEL

GEMINI_URL = "https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"


async def generate(prompt: str) -> str:
    url = GEMINI_URL.format(model=VERTEX_MODEL)
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            url,
            params={"key": GEMINI_API_KEY},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        data = resp.json()
        if "candidates" not in data:
            raise ValueError(f"Gemini API error: {data}")
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        print(f"[GEMINI RAW] {text[:200]}")
        return text