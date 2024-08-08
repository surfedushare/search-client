from tests.base import BaseOpenSearchTestCase


class TestRecordsSearchResultsKeySearchClient(BaseOpenSearchTestCase):

    def test_precise(self):
        totals = self.instance.parse_results_total({"value": 1, "relation": "eq"})
        self.assertEqual(totals["results_total"]["value"], 1)
        self.assertTrue(totals["results_total"]["is_precise"], "Expected relation eq to indicate precise results")

    def test_lower_bound(self):
        totals = self.instance.parse_results_total({"value": 10001, "relation": "gte"})
        self.assertEqual(totals["results_total"]["value"], 10001)
        self.assertFalse(totals["results_total"]["is_precise"], "Expected relation gte to indicate estimated results")
