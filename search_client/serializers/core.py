from __future__ import annotations

from typing import ClassVar, Pattern
from enum import Enum
import re

from pydantic import BaseModel, Field


class EntityStates(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    SKIPPED = "skipped"


class Provider(BaseModel):
    name: str | None = Field(default=None)
    external_id: str | None = Field(default=None)
    slug: str | None = Field(default=None)
    ror: str | None = Field(default=None)


class Highlight(BaseModel):
    description: list[str] | None = Field(default=None)
    text: list[str] | None = Field(default=None)


class StarRatings(BaseModel):
    average: float = Field(default=0.0)
    star_1: int = Field(default=0)
    star_2: int = Field(default=0)
    star_3: int = Field(default=0)
    star_4: int = Field(default=0)
    star_5: int = Field(default=0)


class Metrics(BaseModel):
    views: int = Field(default=0)
    stars: StarRatings


class SearchTermExplanation(BaseModel):

    term: str
    fields: dict[str, float]
    score: float | None = Field(default=None)
    relevancy: float | None = Field(default=None)

    _explanation_description_pattern: ClassVar[Pattern[str]] = re.compile(
        r"(?P<field>\w+(?:\.\w+)*):(?P<term>[^\s)]+)"
    )

    def update(self, total_score: float, score_precision: int = 5) -> None:
        self.score = round(sum(self.fields.values()), score_precision)
        self.relevancy = round(self.score / total_score, 2)

    @classmethod
    def parse_explanation_description(cls, description: str) -> tuple[str, str]:
        matches = cls._explanation_description_pattern.finditer(description)
        matches = list(matches)
        if not matches:
            raise ValueError(f"Expected weight description but got: {description}")
        # Concatenate matches to a single field and term
        field = None
        term = ""
        for match in matches:
            field = match.group("field")
            term += match.group("term") + " | "
        term = term.strip(" | ")
        return field, term

    def __lt__(self, other: SearchTermExplanation) -> bool:
        if self.score is None:
            raise RuntimeError("Can't sort SearchTermExplanation without calling update first.")
        if not isinstance(other, SearchTermExplanation):
            return NotImplemented
        return self.score < other.score


class SearchResultExplanation(BaseModel):
    srn: str
    total_score: float
    terms: list[SearchTermExplanation]
    recency_bonus: float
