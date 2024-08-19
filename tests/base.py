import os
from unittest import TestCase

from opensearchpy import OpenSearch

from configuration import create_configuration
from search_client.constants import DocumentTypes, Platforms, Entities
from search_client.factories import generate_nl_material, generate_nl_product, generate_project, generate_product
from search_client.opensearch import SearchClient, OpenSearchClientBuilder
from search_client.opensearch.indices import build_products_index_configuration, build_projects_index_configuration
from search_client.opensearch.indices.legacy import create_open_search_index_configuration


TEST_INDEX_CONFIGURATIONS = {
    "test-edusources-nl:multilingual-indices": create_open_search_index_configuration(
        "nl", DocumentTypes.LEARNING_MATERIAL
    ),
    "test-publinova-nl:multilingual-indices": create_open_search_index_configuration(
        "nl", DocumentTypes.RESEARCH_PRODUCT
    ),
    "test-edusources-products:default": build_products_index_configuration(DocumentTypes.LEARNING_MATERIAL),
    "test-publinova-products:default": build_products_index_configuration(DocumentTypes.RESEARCH_PRODUCT),
    "test-publinova-projects:default": build_projects_index_configuration(),
}


class BaseSearchClientIntegrationTestCase(TestCase):
    """
    A base TestCase meant to do integration testing with the (SURF) SearchClient

    This test case will, when given a platform, presets list and OpenSearch client:
     * Create test indices with the correct schema.
     * Create a (SURF) SearchClient with the correct SearchConfiguration.
     * Provide an index_document method that allows you to add documents to the index, with custom data if needed.
    """

    # Attributes that should be set by inheriting classes
    platform: Platforms
    presets: list[str] = []
    search: OpenSearch
    alias_prefix: str = "test"

    # Attributes that get set by setUpClass
    instance: SearchClient = None
    aliases: dict[Entities | str, str] = None
    subtypes: dict[Entities, str] = None

    @classmethod
    def setup_opensearch_client(cls) -> OpenSearch:
        raise NotImplementedError("Please override setup_opensearch_client and return a OpenSearch client.")

    @classmethod
    def _get_index_configuration(cls, entity: Entities):
        index_configuration_key = f"{cls.aliases[entity]}:{cls.subtypes[entity]}"
        try:
            return TEST_INDEX_CONFIGURATIONS[index_configuration_key]
        except KeyError:
            raise RuntimeError(f"Test index configuration not available: {index_configuration_key}")

    @classmethod
    def _setup_indices(cls):
        if not cls.instance.configuration.allow_multi_entity_results:
            aliases = cls.instance.configuration.get_aliases_by_language()
            cls.aliases = {Entities.PRODUCTS: aliases.pop("nl")}
            # Here we set aliases for "en" and "unk" that will remain empty during tests, but need to exist.
            for language, alias in aliases.items():
                cls.aliases[language] = alias
        else:
            cls.aliases = {}
            for alias in cls.instance.configuration.get_aliases():
                prefix, platform, entity = alias.split("-")
                entity = Entities(entity)
                cls.aliases[entity] = alias
        for entity, alias in cls.aliases.items():
            if isinstance(entity, str):  # legacy indices that need creation, but remain empty
                entity = Entities.PRODUCTS
            cls.search.indices.create(alias, ignore=400, body=cls._get_index_configuration(entity))

    @classmethod
    def _setup_preset_subtypes(cls):
        cls.subtypes = {}
        for preset in cls.presets:
            entity, subtype = preset.split(":")
            entity = Entities(entity)
            if entity in cls.subtypes:
                raise RuntimeError("Can't test same entity with multiple subtypes in one integration TestCase.")
            cls.subtypes[entity] = subtype

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.search = cls.setup_opensearch_client()
        cls._setup_preset_subtypes()
        cls.instance = SearchClient(cls.search, cls.platform, presets=cls.presets)
        cls.instance.configuration.alias_prefix = cls.alias_prefix
        cls._setup_indices()

    @classmethod
    def tearDownClass(cls):
        for alias in cls.aliases.values():
            cls.search.indices.delete(alias)
        cls.search.close()
        cls.instance.client.close()
        super().tearDownClass()

    @classmethod
    def index_document(cls, entity: Entities, is_last_entity_document: bool = False, **kwargs):
        subtype = cls.subtypes[entity]
        match cls.platform, entity, subtype:
            case Platforms.EDUSOURCES, Entities.PRODUCTS, "multilingual-indices":
                generate_document = generate_nl_material
            case Platforms.PUBLINOVA, Entities.PRODUCTS, "multilingual-indices":
                generate_document = generate_nl_product
            case Platforms.PUBLINOVA, Entities.PRODUCTS, "default":
                generate_document = generate_product
            case Platforms.PUBLINOVA, Entities.PROJECTS, "default":
                generate_document = generate_project
            case _:
                raise ValueError(f"Invalid entity to index_document: {entity.value}")
        body = generate_document(**kwargs)
        index_kwargs = {
            "id": body["srn"],
            "index": cls.aliases[entity],
            "body": body
        }
        if is_last_entity_document:
            index_kwargs["refresh"] = True
        cls.search.index(**index_kwargs)


class SearchClientIntegrationTestCase(BaseSearchClientIntegrationTestCase):

    @classmethod
    def setup_opensearch_client(cls) -> OpenSearch:
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = create_configuration(project_location=project_location)
        return OpenSearchClientBuilder.from_host(config.open_search.url).build()


class SearchClientTestCase(TestCase):
    """
    A base test case to unittest methods on the SearchClient that don't require functional indices.
    """

    instance = None
    platform = Platforms.EDUSOURCES

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = create_configuration(project_location=project_location)
        opensearch_client = OpenSearchClientBuilder.from_host(config.open_search.url).build()
        cls.instance = SearchClient(opensearch_client, cls.platform)
