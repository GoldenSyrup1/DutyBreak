import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(Path(__file__).parent.parent / ".env")

# Google Cloud / Vertex AI
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
VERTEX_MODEL = os.getenv("VERTEX_MODEL", "gemini-2.0-flash")

# Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "trade_regulations")

# External APIs
COMTRADE_API_KEY = os.getenv("COMTRADE_API_KEY", "")
WTO_API_BASE = "https://api.wto.org/timeseries/v1"
OFAC_SDN_URL = "https://www.treasury.gov/ofac/downloads/sdn.xml"

# App
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
