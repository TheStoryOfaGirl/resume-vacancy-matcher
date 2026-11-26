import asyncio
import time

from ..domain.models import OneShotReport
from ..domain.prompts import ONESHOT_TASK
from ..llm.structured import ask_json
from ..tracing import RunResult, StepLog, payload

async def workflow_one_shot(resume_text: str, vacancy_text: str) -> RunResult:
    t0 = time.perf_counter()
    trace: list[StepLog] = []
    try:
        rep = await asyncio.to_thread(
            ask_json,
            OneShotReport,
            ONESHOT_TASK,
            payload(resume_text, vacancy_text),
            trace,
            "one_shot",
        )
        return RunResult("one_shot", rep, time.perf_counter() - t0, trace)
    except Exception as exc:
        return RunResult(
            "one_shot", None, time.perf_counter() - t0, trace,
            error=f"{type(exc).__name__}: {str(exc)[:200]}",
        )