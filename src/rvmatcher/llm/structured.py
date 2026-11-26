import json
import time
from pydantic import BaseModel
from gigachat.models import Chat, Messages, MessagesRole

from .client import get_client
from ..config import MODEL, MAX_OUTPUT_TOKENS
from ..domain.prompts import COMMON_RULES
from ..tracing import StepLog

def ask_json(
    schema: type[BaseModel],
    instruction: str,
    data: dict,
    trace: list[StepLog],
    stage: str,
) -> BaseModel:
    started = time.perf_counter()
    schema_text = json.dumps(schema.model_json_schema(), ensure_ascii=False)
    system_prompt = (
        COMMON_RULES
        + "\nЗадача: " + instruction
        + "\nJSON Schema: " + schema_text
    )
    user_content = json.dumps(data, ensure_ascii=False)

    chat = Chat(
        model=MODEL,
        messages=[
            Messages(role=MessagesRole.SYSTEM, content=system_prompt),
            Messages(role=MessagesRole.USER, content=user_content),
        ],
        temperature=0,
        max_tokens=MAX_OUTPUT_TOKENS,
        response_format={
            "type": "json_schema",
            "schema": schema.model_json_schema(),
            "strict": True,
        },
    )

    try:
        resp = get_client().chat(chat)
        raw = resp.choices[0].message.content
        if not raw:
            raise ValueError("Модель вернула пустой ответ")

        parsed = schema.model_validate_json(raw)

        usage = getattr(resp, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None

        trace.append(StepLog(
            stage,
            time.perf_counter() - started,
            prompt_tokens,
            completion_tokens,
            True,
        ))
        return parsed

    except Exception as exc:
        trace.append(StepLog(
            stage,
            time.perf_counter() - started,
            None, None, False,
            f"{type(exc).__name__}: {str(exc)[:200]}",
        ))
        raise