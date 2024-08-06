from tests.base import BaseOpenSearchTestCase
from search_client.constants import DocumentTypes
from search_client.opensearch import SearchClient, OpenSearchClientBuilder


class TestRecordsSearchResultsKeySearchClient(BaseOpenSearchTestCase):

    document_type = DocumentTypes.LEARNING_MATERIAL

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opensearch_client = OpenSearchClientBuilder.from_host(cls.config.open_search.url).build()
        cls.instance = SearchClient(
            opensearch_client,
            cls.document_type,
            cls.config.open_search.alias_prefix,
        )

    def test_precise(self):
        totals = self.instance.parse_results_total({"value": 1, "relation": "eq"})
        self.assertEqual(totals["results_total"]["value"], 1)
        self.assertTrue(totals["results_total"]["is_precise"], "Expected relation eq to indicate precise results")

    def test_lower_bound(self):
        totals = self.instance.parse_results_total({"value": 10001, "relation": "gte"})
        self.assertEqual(totals["results_total"]["value"], 10001)
        self.assertFalse(totals["results_total"]["is_precise"], "Expected relation gte to indicate estimated results")
