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
