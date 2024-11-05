from enum import Enum

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
