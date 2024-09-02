from typing import Literal
from datetime import datetime, date

from pydantic import (BaseModel, Field, field_serializer, computed_field, field_validator, ValidationInfo,
                      model_validator)
from pydantic.networks import HttpUrl

from search_client.constants import Entities
from search_client.serializers.core import EntityStates, Provider, Highlight
from search_client.serializers.files import Video, Previews, File
from search_client.serializers.persons import Author


class Product(BaseModel):

    entity: Literal[Entities.PRODUCTS] = Field(default=Entities.PRODUCTS, init=False)

    srn: str
    set: str
    external_id: str
    state: EntityStates = Field(default=EntityStates.ACTIVE)
    provider: Provider | None = Field(default=None)
    score: float = Field(default=0)
    published_at: datetime | None = Field(default=None, validation_alias="publisher_date")
    modified_at: datetime | None = Field(default=None)
    url: HttpUrl | None = Field(default=None)
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    language: str | None = Field(default=None)
    copyright: str | None = Field(default=None, deprecated="copyright is deprecated in favor of licenses")
    licenses: list[str] = Field(default_factory=list)
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

    @field_serializer("published_at", "modified_at")
    def serialize_date_field(self, value: datetime, _info) -> date:
        if not value or type(value) is date:
            return value
        return value.date()

    @classmethod
    def _validate_multilingual_text_field(cls, texts: dict, field_name: str) -> str | None:
        values = texts.get(f"{field_name}s")
        if not values:
            return
        return values[0]["text"]

    @model_validator(mode="before")
    @classmethod
    def validate_multilingual_text_fields(cls, values: dict, _info):
        texts = values.get("texts")
        if not texts:
            return values
        language = values.get("language", "unk")
        for field_name in ["title", "subtitle", "description"]:
            values[field_name] = cls._validate_multilingual_text_field(texts[language], field_name)
        return values


class LearningMaterial(Product):
    lom_educational_levels: list[str] = Field(default_factory=list)
    disciplines: list[str] = Field(default_factory=list, validation_alias="disciplines_normalized")
    study_vocabulary: list[str] = Field(default_factory=list)
    technical_type: str | None = Field(default=None,
                                       deprecated="technical_type is deprecated in favor or technical_types")
    technical_types: list[str] = Field(default_factory=list)
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

    type: str | None = Field(default=None, validation_alias="technical_type",
                             deprecated="type is deprecated in favor or types")
    types: list[str] = Field(default_factory=list, validation_alias="technical_types")
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
