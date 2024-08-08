from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from search_client.serializers.persons import Contact


class ProjectStatus(Enum):
    FINISHED = "finished"
    ONGOING = "ongoing"


class Project(BaseModel):
    external_id: str | None = Field(default=None)
    title: str
    description: str
    status: ProjectStatus
    started_at: datetime | None = Field(default=None)
    ended_at: datetime | None = Field(default=None)
    coordinates: list[float] = Field(default_factory=list)
    goal: str | None = Field(default=None)
    contacts: list[Contact] = Field(default_factory=list)
    owners: list[Contact] = Field(default_factory=list)
    persons: list[Contact] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    parties: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)
    research_themes: list[str] = Field(default_factory=list)
