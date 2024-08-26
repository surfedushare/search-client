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

    def test_stats(self):
        stats = self.instance.stats()
        self.assertEqual(stats, {
            "documents": 2,
            "products": 1,
            "projects": 1
        })

    def test_author_suggestions(self):
        self.assertRaises(RuntimeError, self.instance.author_suggestions, "Test Auteur")

    def test_more_like_this(self):
        self.assertRaises(RuntimeError, self.instance.more_like_this, "abc123", "nl")
