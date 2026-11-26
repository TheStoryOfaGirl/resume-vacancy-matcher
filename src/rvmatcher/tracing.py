from dataclasses import dataclass
from .domain.models import MatchReport

@dataclass
class StepLog:
    stage: str
    latency_s: float
    prompt_tokens: int | None
    completion_tokens: int | None
    success: bool
    error: str | None = None

@dataclass
class RunResult:
    workflow: str
    report: MatchReport | None
    wall_time_s: float
    trace: list[StepLog]
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.report is not None and self.error is None

    @property
    def api_calls(self) -> int:
        return len(self.trace)

    @property
    def tokens(self) -> int:
        return sum((s.prompt_tokens or 0) + (s.completion_tokens or 0) for s in self.trace)

def payload(resume_text: str, vacancy_text: str, **extra) -> dict:
    return {"resume_text": resume_text, "vacancy_text": vacancy_text, **extra}