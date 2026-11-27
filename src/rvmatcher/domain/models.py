from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

Verdict = Literal["strong_match", "partial_match", "weak_match"]

class VacancyRequirements(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    title: str = Field(min_length=3, max_length=200)
    seniority: Literal["junior", "middle", "senior", "lead"]
    required_skills: list[str] = Field(min_length=0)
    nice_to_have: list[str] = Field(default_factory=list)
    min_experience_years: float | None = Field(default=None, ge=0, le=50)
    education: str | None = Field(default=None, max_length=300)
    remote: bool = Field(default=False)
    openings: int = Field(default=1, ge=1, le=100)

    @field_validator("required_skills", "nice_to_have")
    @classmethod
    def skills_not_empty_strings(cls, v):
        cleaned = [s.strip() for s in v if s and s.strip()]
        if not cleaned:
            raise ValueError("Список навыков не должен содержать пустых строк")
        return cleaned

    @model_validator(mode="after")
    def experience_consistent_with_seniority(self):
        if self.seniority == "senior" and self.min_experience_years is None:
            raise ValueError("Для senior-позиции min_experience_years должен быть указан")
        return self

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