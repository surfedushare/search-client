from typing import Literal

from pydantic import BaseModel, Field, field_serializer
from search_client.constants import Entities
from search_client.serializers.core import Provider, EntityStates


class BaseOrganization(BaseModel):
    srn: str
    name: str | None = Field(default=None)
    ror: str | None = Field(default=None, description="Research Organization Registry identifier")
    is_root: bool | None = Field(default=None)


class GenericOrganization(BaseModel):
    name: str
    srn: str | None = Field(default=None)  # outside of education context a global identifier will often be missing
    ror: str | None = Field(default=None, description="Research Organization Registry identifier")


class Organization(BaseOrganization):

    entity: Literal[Entities.ORGANIZATIONS] = Field(default=Entities.ORGANIZATIONS, init=False)
    set: str
    provider: Provider | str | None = Field(default=None)
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    score: float = Field(default=0)

    description: str | None = Field(default=None)

    type: str | None = Field(default=None)
    secretary: BaseOrganization | None = Field(default=None, description="Secretary of collaboration organization")
    parents: list[BaseOrganization] = Field(
        default_factory=list,
        description="Parent organizations within educational context"
    )
    members: list[GenericOrganization] = Field(
        default_factory=list,
        description="Members of collaboration organizations possibly from outside the educational context"
    )

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
