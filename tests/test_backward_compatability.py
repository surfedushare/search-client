from tests.base import BaseOpenSearchTestCase
from search_client import SearchClient, DocumentTypes
from search_client.factories import generate_nl_material


class TestRecordsSearchResultsKeySearchClient(BaseOpenSearchTestCase):

    document_type = DocumentTypes.LEARNING_MATERIAL

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.instance = SearchClient(
            cls.config.open_search.url,
            cls.document_type,
            cls.config.open_search.alias_prefix,
            search_results_key="records"
        )

        cls.search.index(index=cls.get_alias("nl"), body=generate_nl_material(), refresh=True)

    def test_search(self):
        search_result = self.instance.search("")
        self.assertIsNotNone(search_result)
        self.assertEqual(
            set(search_result.keys()),
            {"recordcount", "records_total", "records", "drilldowns", "did_you_mean"}
        )
        self.assertIsInstance(search_result["recordcount"], int)
        self.assertIsInstance(search_result["records_total"], dict)
        self.assertIsInstance(search_result["records"], list)

    def test_drilldowns(self):
        drilldowns = self.instance.drilldowns(drilldown_names=[])
        self.assertIsNotNone(drilldowns)
        self.assertEqual(
            set(drilldowns.keys()),
            {"recordcount", "records_total", "records", "drilldowns", "did_you_mean"}
        )
        self.assertIsInstance(drilldowns["recordcount"], int)
        self.assertIsInstance(drilldowns["records_total"], dict)
        self.assertIsInstance(drilldowns["records"], list)

    def test_more_like_this(self):
        more_like_this = self.instance.more_like_this("3522b79c-928c-4249-a7f7-d2bcb3077f10", "nl")
        self.assertIsNotNone(more_like_this)
        self.assertEqual(set(more_like_this.keys()), {"records_total", "results_total", "results"})
        self.assertIsInstance(more_like_this["records_total"], int)
        self.assertIsInstance(more_like_this["results_total"], dict)
        self.assertIsInstance(more_like_this["results"], list)

    def test_author_suggestions(self):
        suggestions = self.instance.author_suggestions("Theo")
        self.assertIsNotNone(suggestions)
        self.assertEqual(set(suggestions.keys()), {"records_total", "results_total", "results"})
        self.assertIsInstance(suggestions["records_total"], int)
        self.assertIsInstance(suggestions["results_total"], dict)
        self.assertIsInstance(suggestions["results"], list)

    def test_legacy_external_id_prefixes(self):
        self.assertEqual(
            self.instance.clean_external_id("edurep_delen:abc"), "urn:uuid:abc",
            "Expected edurep_delen prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("wikiwijsmaken:abc"), "jsonld-from-lom:wikiwijsmaken:abc",
            "Expected wikiwijsmaken prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("l4l:oai:library.wur.nl:l4l/123"),
            "jsonld-from-lom:l4l:oai:library.wur.nl:l4l/123",
            "Expected l4l prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("WikiwijsDelen:urn:uuid:abc"), "urn:uuid:abc",
            "Expected WikiwijsDelen prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("urn:uuid:abc"),
            "urn:uuid:abc", "Expected urn:uuid prefix to be left alone"
        )
        self.assertEqual(self.instance.clean_external_id("abc"), "abc", "Expected Sharekit prefixes to be left alone")
