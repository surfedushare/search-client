from datetime import datetime, date

from pydantic import BaseModel, Field, field_serializer, computed_field, field_validator, ValidationInfo
from pydantic.networks import HttpUrl

from search_client.serializers.core import EntityStates, Provider, Highlight
from search_client.serializers.files import Video, Previews, File
from search_client.serializers.persons import Author


class Product(BaseModel):
    srn: str
    set: str
    external_id: str
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    provider: Provider | None = Field(default=None)
    score: float = Field(default=0)
    published_at: datetime | None = Field(default=None, validation_alias="publisher_date")
    modified_at: date | None = Field(default=None)
    url: HttpUrl
    title: str
    description: str
    language: str
    copyright: str
    video: Video | None = Field(default=None)
    harvest_source: str
    previews: Previews | None = Field(default=None)
    files: list[File] = Field(default_factory=list)
    authors: list[Author] = Field(default_factory=list)
    has_parts: list[str] = Field(default_factory=list)
    is_part_of: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    doi: str | None = Field(default=None)
    subtitle: str | None = Field(default=None)
    highlight: Highlight | None = Field(default=None)

    @field_serializer("provider")
    def serialize_provider(self, provider: Provider, _info) -> str:
        if provider.name:
            return provider.name
        elif provider.slug:
            return provider.slug
        elif provider.ror:
            return provider.ror
        elif provider.external_id:
            return provider.external_id


class LearningMaterial(Product):
    lom_educational_levels: list[str] = Field(default_factory=list)
    disciplines: list[str] = Field(default_factory=list, validation_alias="disciplines_normalized")
    study_vocabulary: list[str] = Field(default_factory=list)
    technical_type: str | None = Field(default=None)
    material_types: list[str] = Field(default_factory=list)
    aggregation_level: str | None = Field(default=None)
    publishers: list[str] = Field(default_factory=list)
    consortium: str | None = Field(default=None)

    @field_validator("disciplines", "study_vocabulary", "consortium", mode="before")
    @classmethod
    def validate_multilingual_terms_field(cls, value: dict | list, info: ValidationInfo):
        if not isinstance(value, dict):
            return value
        elif "keyword" not in value:
            raise ValueError(f"multilingual_terms_field '{info.field_name}' did not specify a keyword property")
        return value["keyword"]


class ResearchProduct(Product):

    type: str = Field(validation_alias="technical_type")
    research_object_type: str | None = Field(default=None)
    parties: list[str] = Field(default_factory=list, validation_alias="publishers")
    research_themes: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)

    @field_serializer("doi")
    def serialize_doi(self, doi: str, _info):
        if not doi:
            return
        return f"https://doi.org/{doi}"

    @field_serializer("subtitle")
    def serialize_subtitle(self, subtitle: str, _info):
        if not subtitle:
            return
        return subtitle if subtitle not in self.title else None

    def _list_first_author(self):
        if not self.authors:
            return []
        return [self.authors[0]]

    @computed_field
    @property
    def owners(self) -> list[Author]:
        return self._list_first_author()

    @computed_field
    @property
    def contacts(self) -> list[Author]:
        return self._list_first_author()
