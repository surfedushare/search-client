from search_client.constants import Platforms, Entities, SEARCH_FIELDS, DocumentTypes
from search_client.serializers.products import LearningMaterial, ResearchProduct
from search_client.opensearch.configuration.core import SearchConfiguration


class ProductSearchConfiguration(SearchConfiguration):
    pass


def build_product_search_configuration(platform: Platforms) -> SearchConfiguration:
    if platform is Platforms.EDUSOURCES:
        document_type = DocumentTypes.LEARNING_MATERIAL
        serializer = LearningMaterial
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
        }
    )
