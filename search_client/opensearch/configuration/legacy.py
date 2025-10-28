from typing import Type

from pydantic import BaseModel

from search_client.constants import Platforms, Entities, SEARCH_FIELDS, LANGUAGES, DocumentTypes
from search_client.serializers.products import LearningMaterial, ResearchProduct
from search_client.opensearch.configuration.core import SearchConfiguration


class MultilingualIndicesSearchConfiguration(SearchConfiguration):

    allow_multi_entity_results = False
    use_aggregations_over_drilldowns = False

    def get_aliases(self) -> list[str]:
        alias_prefix = "" if not self.alias_prefix else f"{self.alias_prefix}-"
        return [f"{alias_prefix}{self.platform.value}-{language}" for language in LANGUAGES]

    def get_aliases_by_entity(self) -> dict[Entities, str]:
        raise NotImplementedError("Can't group language based aliases by an entity")

    def get_aliases_by_language(self) -> dict[str, str]:
        alias_prefix = "" if not self.alias_prefix else f"{self.alias_prefix}-"
        return {
            language: f"{alias_prefix}{self.platform.value}-{language}"
            for language in LANGUAGES
        }

    def get_serializer_from_index(self, index: str) -> Type[BaseModel]:
        assert len(self.entities) == 1, \
            f"Expected exactly one entity to get a serializer from index, but found: {self.entities}"
        entity = next(iter(self.entities))
        return self.serializers[entity]


def build_multilingual_indices_search_configuration(platform: Platforms) -> SearchConfiguration:
    filter_fields = {
        "publisher_year_normalized", "authors.name.keyword", "language.keyword", "copyright.keyword",
        "publishers.keyword", "technical_type", "publisher_year"
    }
    if platform is Platforms.EDUSOURCES:
        document_type = DocumentTypes.LEARNING_MATERIAL
        serializer = LearningMaterial
        filter_fields |= {
            "study_vocabulary", "learning_material_disciplines_normalized",  # these are deprecated
            "lom_educational_levels", "consortium.keyword", "material_types", "aggregation_level"
        }
    elif platform is Platforms.PUBLINOVA:
        document_type = DocumentTypes.RESEARCH_PRODUCT
        serializer = ResearchProduct
        filter_fields |= {"research_object_type", "research_themes", "has_material"}
    else:
        raise ValueError(f"Can't build product search configuration for platform: {platform}")
    return MultilingualIndicesSearchConfiguration(
        platform=platform,
        entities={Entities.PRODUCTS},
        search_fields=SEARCH_FIELDS[document_type],
        serializers={Entities.PRODUCTS: serializer},
        filter_fields=filter_fields,
        range_filter_fields={"publisher_date"},  # this is deprecated
        distance_feature_field="publisher_date",  # this is deprecated
        highlights={
            "description": {"description"},
            "text": {"text"}
        },
        more_like_this_field_references={"title", "description"},
    )
