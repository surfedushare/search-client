from __future__ import annotations

from typing import ClassVar
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

    _explanation_description_pattern: ClassVar[str] = re.compile(r"^weight\((?P<field>.+):(?P<term>.+) in \d+\)")

    def update(self, total_score: float, score_precision: int = 5) -> None:
        self.score = round(sum(self.fields.values()), score_precision)
        self.relevancy = round(self.score / total_score, 2)

    @classmethod
    def parse_explanation_description(cls, description: str) -> tuple[str, str]:
        match = cls._explanation_description_pattern.match(description)
        if not match:
            raise ValueError(f"Expected weight description but got: {description}")
        # closing_parenthesis = description.find(" in 0)")
        # clean_description = description[:closing_parenthesis].replace("weight(", "")
        # split_description = clean_description.split(":")
        # assert len(split_description) == 2, f"Expected description to contain 2 part but got: {split_description}"
        return match.group("field"), match.group("term")

    def __lt__(self, other: SearchTermExplanation) -> bool:
        if self.score is None:
            raise RuntimeError("Can't sort SearchTermExplanation without calling update first.")
        if not isinstance(other, SearchTermExplanation):
            return NotImplemented
        return self.score < other.score


class SearchResultExplanation(BaseModel):
    id: str
    total_score: float
    terms: list[SearchTermExplanation]
    recency_bonus: float
