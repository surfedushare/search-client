from __future__ import annotations

from typing import Type, ClassVar
from dataclasses import dataclass, field

from pydantic import BaseModel

from search_client.constants import Platforms, Entities, LANGUAGES


@dataclass(slots=True)
class SearchConfiguration:

    platform: Platforms
    entities: set[Entities]
    search_fields: list[str]
    serializers: dict[Entities, Type[BaseModel]]
    filter_fields: set[str] = field(default_factory=set)
    range_filter_fields: set[str] = field(default_factory=set)
    distance_feature_field: str | None = field(default="published_at")
    more_like_this_field_references: set[str] = field(default_factory=set)
    highlights: dict[str, set[str]] | None = None  # values are field references

    alias_prefix: str | None = field(default=None)

    allow_multi_entity_results: ClassVar[bool] = True
    use_aggregations_over_drilldowns: ClassVar[bool] = True

    def get_aliases(self) -> list[str]:
        return list(self.get_aliases_by_entity().values())

    def get_aliases_by_entity(self) -> dict[Entities, str]:
        alias_prefix = "" if not self.alias_prefix else f"{self.alias_prefix}-"
        return {
            entity: f"{alias_prefix}{self.platform.value}-{entity.value}"
            for entity in self.entities
        }

    def get_aliases_by_language(self) -> dict[str, str]:
        assert len(self.entities) == 1, \
            f"Expected exactly one entity to generate indices by language, but found: {self.entities}"
        entity = next(iter(self.entities))
        alias_prefix = "" if not self.alias_prefix else f"{self.alias_prefix}-"
        return {
            language: f"{alias_prefix}{self.platform.value}-{entity.value}"
            for language in LANGUAGES
        }

    def get_serializer_from_index(self, index: str) -> Type[BaseModel]:
        if not self.alias_prefix:
            platform, entity = index.split("-")
        else:
            prefix, platform, entity = index.split("-")
        entity = Entities(entity)
        return self.serializers[entity]

    def get_valid_filter_fields(self) -> set[str]:
        return self.filter_fields | self.range_filter_fields

    @staticmethod
    def interpolate_field_languages(*args: str) -> list[str]:
        """
        This method takes field references like "texts:titles" and returns valid fields for all languages.
        In the example above that would be ["texts.nl.titles.text", "texts.en.titles.text", "texts.unk.titles.text"]

        :param args: Field references.
        :return: Valid fields for each reference in each language that the configuration/index supports.
        """
        field_names = []
        for field_reference in args:
            # If the reference doesn't start with the correct prefix, we assume it's already a valid field
            if not field_reference.startswith("texts:"):
                field_names.append(field_reference)
                continue
            _, subfield = field_reference.split(":")
            for language in LANGUAGES:
                field_names.append(f"texts.{language}.{subfield}.text")
        return field_names

    @staticmethod
    def extrapolate_field_references(*args: str) -> list[str]:
        """
        This method takes field names and will extract the field reference(s) from them by stripping language specifics.
        The reference for "texts.nl.titles.text", "texts.en.titles.text" and "texts.unk.titles.text" is "texts:titles".

        :param args: Field names.
        :return: References
        """
        references = set()
        for field_name in args:
            # If the field name doesn't start with the correct prefix, we assume it's a valid field.
            # In this way field names may get mixed with references.
            if not field_name.startswith("texts."):
                references.add(field_name)
                continue
            _, _, subfield, _ = field_name.split(".")
            references.add(f"texts:{subfield}")
        references = list(references)
        references.sort()
        return references

    def get_highlight_fields(self) -> list[str]:
        fields = []
        for field_references in self.highlights.values():
            fields += self.interpolate_field_languages(*field_references)
        return fields

    def merge(self, other: SearchConfiguration) -> None:
        # Some defensive type checking to prevent accidents
        assert isinstance(other, SearchConfiguration), f"Can't merge a SearchConfiguration with a {type(other)}"
        assert self.platform == other.platform, "Can't merge SearchConfigurations from different platforms"
        assert self.allow_multi_entity_results and other.allow_multi_entity_results, \
            "SearchConfiguration doesn't allow for multi entity search results, refusing to merge configurations"
        for entity in self.entities:
            assert entity not in other.entities, f"Can't merge SearchConfigurations with overlapping entity '{entity}'"
        for entity in self.serializers:
            assert entity not in other.serializers, \
                f"Can't merge SearchConfigurations with overlapping serializer for entity '{entity}'"

        self.entities |= other.entities  # union
        self.search_fields += other.search_fields  # concatenation of lists
        self.serializers.update(other.serializers)  # dict update
        self.filter_fields &= other.filter_fields  # intersection
        self.range_filter_fields &= other.range_filter_fields  # intersection
        # If distance_feature_fields don't match we unset the variable, because we can't process that.
        if self.distance_feature_field != other.distance_feature_field:
            self.distance_feature_field = None
