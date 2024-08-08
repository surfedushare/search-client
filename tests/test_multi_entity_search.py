import os
from unittest import TestCase

from pydantic import BaseModel

from configuration import create_configuration
from search_client.constants import Platforms, Entities, DocumentTypes
from search_client.opensearch import SearchClient, OpenSearchClientBuilder
from search_client.opensearch.indices import build_products_index_configuration, build_projects_index_configuration
from search_client.serializers import ResearchProduct, Project
from search_client.factories import generate_nl_product, generate_project


class TestMultiEntitySearchClient(TestCase):

    platform = Platforms.PUBLINOVA
    entities = {
        Entities.PRODUCTS: build_products_index_configuration(
            DocumentTypes.RESEARCH_PRODUCT,
            "dutch-decompound-words.txt"
        ),
        Entities.PROJECTS: build_projects_index_configuration(),
    }

    @classmethod
    def get_alias(cls, entity):
        return f"{cls.platform.value}-{entity.value}"

    @classmethod
    def setUpTestData(cls):
        cls.search.index(
            index=cls.get_alias(Entities.PRODUCTS),
            body=generate_nl_product(),
            refresh=True  # always put refresh on the last document of an index
        )
        cls.search.index(
            index=cls.get_alias(Entities.PROJECTS),
            body=generate_project(),
            refresh=True  # always put refresh on the last document of an index
        )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.config = create_configuration(project_location=project_location)
        cls.search = OpenSearchClientBuilder.from_host(cls.config.open_search.url).build()
        for entity in cls.entities:
            cls.search.indices.create(
                cls.get_alias(entity),
                ignore=400,
                body=cls.entities[entity]
            )
        cls.instance = SearchClient(cls.search, cls.platform, presets=["products:default", "projects:default"])
        cls.setUpTestData()

    @classmethod
    def tearDownClass(cls):
        for entity in cls.entities:
            cls.search.indices.delete(
                cls.get_alias(entity)
            )
        cls.search.close()
        cls.instance.client.close()
        super().tearDownClass()

    def assert_results_total(self, total):
        self.assertIsInstance(total, dict)
        self.assertIn("value", total)
        self.assertIn("is_precise", total)
        self.assertIsInstance(total["value"], int)
        self.assertIsInstance(total["is_precise"], bool)

    def test_basic_search(self):
        search_result = self.instance.search("")
        self.assert_results_total(search_result["results_total"])
        expected_types = {ResearchProduct, Project}
        for result in search_result["results"]:
            expected_types.discard(type(result))
            self.assertIsInstance(result, BaseModel)
        self.assertEqual(expected_types, set(), "Expected ResearchProduct and Project types inside search results.")
