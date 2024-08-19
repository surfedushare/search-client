from pydantic import BaseModel

from tests.base import SearchClientIntegrationTestCase
from search_client.constants import Platforms, Entities
from search_client.serializers import ResearchProduct, Project


class TestMultiEntitySearchClient(SearchClientIntegrationTestCase):

    platform = Platforms.PUBLINOVA
    presets = ["products:default", "projects:default"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index_document(Entities.PRODUCTS, is_last_entity_document=True)
        cls.index_document(Entities.PROJECTS, is_last_entity_document=True)

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
