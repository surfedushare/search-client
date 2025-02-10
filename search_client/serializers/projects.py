from typing import Literal, Any
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_serializer, field_validator

from search_client.constants import Entities
from search_client.serializers.core import EntityStates, Provider
from search_client.serializers.files import Previews
from search_client.serializers.persons import Contact


class ProjectStatus(Enum):
    FINISHED = "finished"
    ONGOING = "ongoing"
    PREPARING = "preparing"
    TO_BE_STARTED = "to be started"  # similar to "preparing", required by Publinova
    UNKNOWN = "unknown"


class Project(BaseModel):

    entity: Literal[Entities.PROJECTS] = Field(default=Entities.PROJECTS, init=False)
    srn: str
    set: str
    provider: Provider | str | None = Field(default=None)
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    score: float = Field(default=0)

    external_id: str | None = Field(default=None)
    title: str
    description: str | None = Field(default=None)
    project_status: ProjectStatus = Field(default=ProjectStatus.UNKNOWN)
    started_at: date | None = Field(default=None)
    ended_at: date | None = Field(default=None)
    coordinates: list[float] = Field(default_factory=list)
    goal: str | None = Field(default=None)
    contacts: list[Contact] = Field(default_factory=list)
    owners: list[Contact] = Field(default_factory=list)
    persons: list[Contact] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    parties: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    previews: Previews | None = Field(default=None)
    sia_project_reference: str | None = Field(default=None)

    @field_serializer("provider")
    def serialize_provider(self, provider: Provider, _info) -> str:
        if isinstance(provider, str):
            return provider
        elif provider.name:
            return provider.name
        elif provider.slug:
            return provider.slug
        elif provider.ror:
            return provider.ror
        elif provider.external_id:
            return provider.external_id

    @field_validator("started_at", "ended_at", mode="before")
    @classmethod
    def convert_to_date(cls, value: Any) -> date:
        if isinstance(value, datetime):
            return value.date()
        return value
