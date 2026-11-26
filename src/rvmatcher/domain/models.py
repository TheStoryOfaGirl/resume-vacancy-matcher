from typing import Literal
from pydantic import BaseModel, Field

Verdict = Literal["strong_match", "partial_match", "weak_match"]

class VacancyRequirements(BaseModel):
    title: str
    required_skills: list[str]
    nice_to_have: list[str]
    min_experience_years: float | None
    education: str | None

class ResumeFacts(BaseModel):
    skills: list[str]
    experience_years: float | None
    positions: list[str]
    education: str | None

class MatchScore(BaseModel):
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: int = Field(ge=0, le=100)
    verdict: Verdict
    risks: list[str]
    needs_human_review: bool

class MatchReport(MatchScore):
    pass

class OneShotReport(MatchScore):
    pass