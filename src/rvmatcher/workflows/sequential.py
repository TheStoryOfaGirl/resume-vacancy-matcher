import asyncio
import time

from ..domain.models import VacancyRequirements, ResumeFacts, MatchScore, MatchReport
from ..domain.prompts import VACANCY_TASK, RESUME_TASK, MATCH_TASK
from ..llm.structured import ask_json, ask_json_with_retry
from ..tracing import RunResult, StepLog, payload

async def workflow_sequential(resume_text: str, vacancy_text: str) -> RunResult:
    t0 = time.perf_counter()
    trace: list[StepLog] = []
    try:
        vac = await asyncio.to_thread(
            ask_json_with_retry, VacancyRequirements, VACANCY_TASK,
            payload(resume_text, vacancy_text), trace, "extract_vacancy",
            max_retries=2,
        )
        res = await asyncio.to_thread(
            ask_json, ResumeFacts, RESUME_TASK,
            payload(resume_text, vacancy_text), trace, "extract_resume",
        )
        score = await asyncio.to_thread(
            ask_json, MatchScore, MATCH_TASK,
            payload(resume_text, vacancy_text,
                    vacancy=vac.model_dump(), resume=res.model_dump()),
            trace, "match",
        )
        return RunResult("sequential", MatchReport(**score.model_dump()),
                         time.perf_counter() - t0, trace)
    except Exception as exc:
        return RunResult(
            "sequential", None, time.perf_counter() - t0, trace,
            error=f"{type(exc).__name__}: {str(exc)[:200]}",
        )