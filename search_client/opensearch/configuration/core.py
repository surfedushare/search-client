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
    distance_feature_field: str | None = field(default="publisher_date")

    allow_multi_entity_results: ClassVar[bool] = True
    use_aggregations_over_drilldowns: ClassVar[bool] = True

    def get_indices(self) -> list[str]:
        return [f"{self.platform.value}-{entity.value}" for entity in self.entities]

    def get_indices_by_language(self) -> dict[str, str]:
        assert len(self.entities) == 1, \
            f"Expected exactly one entity to generate indices by language, but found: {self.entities}"
        entity = next(iter(self.entities))
        return {
            language: f"{self.platform.value}-{entity.value}"
            for language in LANGUAGES
        }

    def get_serializer_from_index(self, index: str) -> Type[BaseModel]:
        platform, entity = index.split("-")
        entity = Entities(entity)
        return self.serializers[entity]

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
        # If distance_feature_fields don't match we unset the variable, because we can't process that.
        if self.distance_feature_field != other.distance_feature_field:
            self.distance_feature_field = None
