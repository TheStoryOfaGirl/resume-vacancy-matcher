from gigachat import GigaChat
from ..config import GIGACHAT_CREDENTIALS, GIGACHAT_BASE_URL, SCOPE, MODEL

_client = None

def get_client() -> GigaChat:
    global _client
    if _client is None:
        _client = GigaChat(
            base_url=GIGACHAT_BASE_URL,
            credentials=GIGACHAT_CREDENTIALS,
            scope=SCOPE,
            model=MODEL,
            verify_ssl_certs=False,
            timeout=60.0,
            max_retries=0,
        )
    return _client