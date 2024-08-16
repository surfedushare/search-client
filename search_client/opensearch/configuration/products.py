from search_client.constants import Platforms, Entities, SEARCH_FIELDS, DocumentTypes
from search_client.serializers.products import LearningMaterial, ResearchProduct
from search_client.opensearch.configuration.core import SearchConfiguration


class ProductSearchConfiguration(SearchConfiguration):
    pass


def build_product_search_configuration(platform: Platforms) -> SearchConfiguration:
    filter_fields = {
        "publisher_year_normalized", "authors.name.keyword", "language.keyword", "copyright.keyword",
        "publishers.keyword", "technical_type", "publisher_year"
    }
    if platform is Platforms.EDUSOURCES:
        document_type = DocumentTypes.LEARNING_MATERIAL
        serializer = LearningMaterial
        filter_fields |= {
            "study_vocabulary.keyword", "disciplines_normalized.keyword",
            "lom_educational_levels", "consortium.keyword", "material_types", "aggregation_level"
        }
    elif platform is Platforms.PUBLINOVA:
        document_type = DocumentTypes.RESEARCH_PRODUCT
        serializer = ResearchProduct
    else:
        raise ValueError(f"Can't build product search configuration for platform: {platform}")
    return ProductSearchConfiguration(
        platform=platform,
        entities={Entities.PRODUCTS},
        search_fields=SEARCH_FIELDS[document_type],
        serializers={
            Entities.PRODUCTS: serializer
        },
        range_filter_fields={"published_at", "modified_at"},
    )
