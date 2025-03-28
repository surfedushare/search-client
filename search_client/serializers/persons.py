from typing import Literal

from pydantic import BaseModel, Field, EmailStr, model_validator, HttpUrl

from search_client.constants import Entities
from search_client.serializers.core import EntityStates, Provider


class Contact(BaseModel):
    name: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None)
    is_external: bool | None = Field(default=None,
                                     description="This means external contact for the Provider of a Project.")

    @model_validator(mode="after")
    def validate_identifier(self):
        if not self.email and not self.external_id:
            raise ValueError("Either email or external_id must be set")
        return self


class Author(BaseModel):
    name: str
    email: EmailStr | None = Field(default=None)
    external_id: str | None = Field(default=None, description="The id of the author in the source system.")
    dai: str | None = Field(default=None)
    isni: str | None = Field(default=None)
    orcid: str | None = Field(default=None)
    is_external: bool | None = Field(default=None,
                                     description="This means external author for the Provider of a Product.")


class Person(BaseModel):

    entity: Literal[Entities.PROJECTS] = Field(default=Entities.PERSONS, init=False)
    srn: str
    set: str
    provider: Provider | str | None = Field(default=None)
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    score: float = Field(default=0)

    name: str
    fist_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    prefix: str | None = Field(default=None)
    initials: str | None = Field(default=None)
    description: str | None = Field(default=None)

    email: EmailStr | None = Field(default=None)
    phone: str | None = Field(default=None)
    photo_url: HttpUrl | None = Field(default=None)

    external_id: str | None = Field(default=None, description="The id of the person in the source system.")
    isni: str | None = Field(default=None)

    skills: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    is_employed: bool | None = Field(default=None)
    job_title: str | None = Field(default=None)


class Researcher(Person):
    title: str | None = Field(default=None, description="The academic title of the researcher.")
    themes: list[str] = Field(default_factory=list, description="The themes of the research fields of the researcher.")
    orcid: str | None = Field(default=None)
    dai: str | None = Field(default=None)
