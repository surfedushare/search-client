from tests.base import SearchClientIntegrationTestCase
from search_client.constants import Platforms, Entities
from search_client.serializers.projects import Project


class TestResearchProjectSearchClient(SearchClientIntegrationTestCase):

    # Attributes used by SearchClientIntegrationTestCase
    platform = Platforms.PUBLINOVA
    presets = ["projects:default"]

    # Attributes for test cases in this file
    aggregation_key = "aggregations"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index_document(Entities.PROJECTS)
        cls.index_document(
            Entities.PROJECTS, is_last_entity_document=True,
            external_id="abc", title="Project Pythagoras", description="Groots zijn zijn projecten",
            project_status="ongoing"
        )

    def get_value_from_result(self, result, key):
        data = result.model_dump()
        value = data[key]
        return value

    def assert_value_from_result(self, result, key, expectation, assertion=None, message=None):
        assertion = assertion or self.assertEqual
        value = self.get_value_from_result(result, key)
        assertion(value, expectation, message)

    def assert_results_total(self, total):
        self.assertIsInstance(total, dict)
        self.assertIn("value", total)
        self.assertIn("is_precise", total)
        self.assertIsInstance(total["value"], int)
        self.assertIsInstance(total["is_precise"], bool)

    def test_basic_search(self):
        search_result = self.instance.search('')
        search_result_filter = self.instance.search(
            '',
            filters=[{"external_id": "project_status", "items": ["ongoing"]}]
        )
        # did we get _anything_ from search?
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result_filter)
        self.assert_results_total(search_result["results_total"])
        self.assert_results_total(search_result_filter["results_total"])
        self.assertGreater(search_result['results_total']['value'], search_result_filter['results_total']['value'])
        self.assertEqual(
            set(search_result.keys()),
            {"results_total", "results", self.aggregation_key, "did_you_mean"}
        )
        # does an empty search return a list?
        self.assertIsInstance(search_result['results'], list)
        # are there no aggregations for an empty search?
        self.assertIsInstance(search_result[self.aggregation_key], dict)
        self.assertEqual(len(search_result[self.aggregation_key]), 0)

        # basic search
        search_pythagoras = self.instance.search("Pythagoras")
        self.assertIsNotNone(search_pythagoras)
        self.assertTrue(search_pythagoras["results"])
        self.assertIsNot(search_result, search_pythagoras)
        self.assertNotEqual(search_result['results_total']['value'], search_pythagoras['results_total']['value'])

        # basic search pagination
        search_page_1 = self.instance.search("", page_size=1)
        self.assertIsNotNone(search_page_1)
        self.assertNotEqual(search_page_1, search_result)
        search_page_2 = self.instance.search("", page=2, page_size=1)
        self.assertIsNotNone(search_page_2)
        self.assertNotEqual(search_page_2, search_page_1)

    def test_aggregation_search(self):
        search_pythagoras = self.instance.search("Pythagoras", drilldown_names=["project_status"])
        self.assertIsNotNone(search_pythagoras)
        self.assertEqual(len(search_pythagoras[self.aggregation_key]), 1)
        for key, value in search_pythagoras[self.aggregation_key].items():
            self.assertIn("-", key)
            self.assertGreater(value, 0)

    def test_autocomplete(self):
        empty_autocomplete = self.instance.autocomplete(query='')
        self.assertEqual(len(empty_autocomplete), 0)
        pythagoras_autocomplete = self.instance.autocomplete(query='wis')
        self.assertGreater(len(pythagoras_autocomplete), 0)
        self.assertIsNot(empty_autocomplete, pythagoras_autocomplete)
        self.assertIsInstance(pythagoras_autocomplete, list)
        for item in pythagoras_autocomplete:
            self.assertIsInstance(item, str)
            self.assertTrue('wiskundig' in item)

    def test_get_documents_by_srn(self):
        test_id = "edurep:project:1"  # factories don't change the platform
        result = self.instance.get_documents_by_srn([test_id])
        self.assertIsNotNone(result)
        self.assertEqual(result['results_total']['value'], 1, "Expected one result when searching for one id")
        document = result['results'][0]
        self.assertIsInstance(document, Project)
        self.assertEqual(document.srn, test_id)

    def test_stats_dict(self):
        stats = self.instance.stats()
        self.assertEqual(stats, {
            "documents": 2,
            "projects": 2
        })
