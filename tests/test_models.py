import pytest
from pydantic import ValidationError
from rvmatcher.domain.models import VacancyRequirements

VALID = {
    "title": "Python-разработчик",
    "seniority": "middle",
    "required_skills": ["Python"],
    "nice_to_have": [],
    "min_experience_years": 3.0,
    "education": None,
    "remote": False,
    "openings": 1,
}

BAD_CASES = [
    ("unknown_extra", {**VALID, "invented": 1}),
    ("empty_skills", {**VALID, "required_skills": []}),
    ("senior_without_experience", {**VALID, "seniority": "senior", "min_experience_years": None}),
    ("invalid_seniority", {**VALID, "seniority": "principal"}),
    ("zero_openings", {**VALID, "openings": 0}),
]

@pytest.mark.parametrize("name,obj", BAD_CASES)
def test_invalid_cases(name, obj):
    with pytest.raises(ValidationError):
        VacancyRequirements.model_validate(obj)