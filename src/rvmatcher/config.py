import os
from dotenv import load_dotenv

load_dotenv()

GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_CREDENTIALS")
if not GIGACHAT_CREDENTIALS:
    raise ValueError("Set GIGACHAT_CREDENTIALS in .env")

GIGACHAT_BASE_URL = "https://api.giga.chat/v1"
SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
MODEL = os.getenv("GIGACHAT_MODEL", "GigaChat-2")
MAX_OUTPUT_TOKENS = 800