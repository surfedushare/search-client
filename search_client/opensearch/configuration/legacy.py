from typing import Type

from pydantic import BaseModel

from search_client.constants import Platforms, Entities, SEARCH_FIELDS, LANGUAGES, DocumentTypes
from search_client.serializers.products import LearningMaterial, ResearchProduct
from search_client.opensearch.configuration.core import SearchConfiguration


class MultilingualIndicesSearchConfiguration(SearchConfiguration):

    def get_indices(self) -> list[str]:
        return [f"{self.platform.value}-{language}" for language in LANGUAGES]

    def get_indices_by_language(self) -> dict[str, str]:
        return {
            language: f"{self.platform.value}-{language}"
            for language in LANGUAGES
        }

    def get_serializer_from_index(self, index: str) -> Type[BaseModel]:
        assert len(self.entities) == 1, \
            f"Expected exactly one entity to get a serializer from index, but found: {self.entities}"
        entity = next(iter(self.entities))
        return self.serializers[entity]


def build_multilingual_indices_search_configuration(platform: Platforms) -> SearchConfiguration:
    if platform is Platforms.EDUSOURCES:
        document_type = DocumentTypes.LEARNING_MATERIAL
        serializer = LearningMaterial
    elif platform is Platforms.PUBLINOVA:
        document_type = DocumentTypes.RESEARCH_PRODUCT
        serializer = ResearchProduct
    else:
        raise ValueError(f"Can't build product search configuration for platform: {platform}")
    return MultilingualIndicesSearchConfiguration(
        platform=platform,
        entities={Entities.PRODUCTS},
        search_fields=SEARCH_FIELDS[document_type],
        serializers={Entities.PRODUCTS: serializer},
        allow_multi_entity_results=False
    )
