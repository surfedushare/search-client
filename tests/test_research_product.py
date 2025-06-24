from datetime import datetime, date

from tests.base import SearchClientIntegrationTestCase
from search_client.constants import Platforms, Entities
from search_client.serializers.products import ResearchProduct


class TestResearchProductSearchClient(SearchClientIntegrationTestCase):

    # Attributes used by SearchClientIntegrationTestCase
    platform = Platforms.PUBLINOVA
    presets = ["products:default"]

    # Attributes for test cases in this file
    aggregation_key = "aggregations"
    datetime_field = "publisher_date"
    highlight_key = "texts:contents"
    has_integer_stats = False

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index_document(Entities.PRODUCTS, source="surfsharekit")
        cls.index_document(
            Entities.PRODUCTS,
            source="surfsharekit", external_id="abc", title="De wiskunde van Pythagoras",
            description="Groots is zijn onderzoek"
        )
        cls.index_document(
            Entities.PRODUCTS,
            source="surfsharekit", copyright="cc-by-40", topic="biology", publisher_date="2018-04-16T22:35:09+02:00"
        )
        cls.index_document(
            Entities.PRODUCTS,
            source="surfsharekit", topic="biology", publisher_date="2019-04-16T22:35:09+02:00", external_id="def",
        )
        cls.index_document(
            Entities.PRODUCTS, is_last_entity_document=True,
            technical_type="video", source="surfsharekit", topic="biology", external_id="123",
        )

    def get_value_from_result(self, result, key):
        data = result.model_dump()
        if key == "technical_type":
            value = data["type"]
        else:
            value = data[key]
        return value

    def assert_value_from_result(self, result, key, expectation, assertion=None, message=None):
        assertion = assertion or self.assertEqual
        if key == "studies":
            return  # silently skipping this assertion, because NPPO doesn't support studies
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
        search_result_filter = self.instance.search('', filters=[{"external_id": "technical_type", "items": ["video"]}])
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
        search_biologie = self.instance.search("biologie")
        self.assertIsNotNone(search_biologie)
        self.assertTrue(search_biologie["results"])
        self.assertIsNot(search_result, search_biologie)
        self.assertNotEqual(search_result['results_total']['value'], search_biologie['results_total']['value'])

        # basic search pagination
        search_page_1 = self.instance.search("", page_size=1)
        self.assertIsNotNone(search_page_1)
        self.assertNotEqual(search_page_1, search_result)
        search_page_2 = self.instance.search("", page=2, page_size=1)
        self.assertIsNotNone(search_page_2)
        self.assertNotEqual(search_page_2, search_page_1)

    def test_filter_search(self):
        # search with single filter applied
        search_biologie_video = self.instance.search(
            "biologie",
            filters=[{"external_id": "technical_type", "items": ["video"]}]
        )
        self.assertTrue(search_biologie_video["results"])
        for result in search_biologie_video["results"]:
            self.assert_value_from_result(result, "technical_type", "video")
        search_biologie_video_and_docs = self.instance.search(
            "biologie",
            filters=[{"external_id": "technical_type", "items": ["video", "document"]}]
        )
        self.assertGreater(
            search_biologie_video_and_docs["results_total"]["value"],
            search_biologie_video["results_total"]["value"]
        )
        for result in search_biologie_video_and_docs["results"]:
            self.assert_value_from_result(result, "technical_type", ["video", "document"], self.assertIn)

        # search with multiple filters applied
        search_biologie_text_and_cc_by = self.instance.search(
            "biologie",
            filters=[
                {"external_id": "technical_type", "items": ["document"]},
                {"external_id": "copyright.keyword", "items": ["cc-by-40"]}
            ]
        )
        self.assertTrue(search_biologie_text_and_cc_by["results"])
        for result in search_biologie_text_and_cc_by["results"]:
            self.assert_value_from_result(result, "technical_type", "document")
            self.assert_value_from_result(result, "copyright", "cc-by-40")

        # AND search with multiple filters applied
        search_biologie_and_didactiek = self.instance.search("biologie didactiek")
        search_biologie_and_didactiek_with_filters = self.instance.search(
            "biologie didactiek",
            filters=[
                {"external_id": "technical_type", "items": ["document"]},
                {"external_id": "copyright.keyword", "items": ["cc-by-40"]}
            ])

        self.assertIsNotNone(search_biologie_and_didactiek)
        self.assertTrue(search_biologie_and_didactiek["results"])
        self.assertIsNot(search_biologie_and_didactiek, search_biologie_and_didactiek_with_filters)
        self.assertTrue(search_biologie_and_didactiek_with_filters["results"])
        self.assertNotEqual(
            search_biologie_and_didactiek['results_total']['value'],
            search_biologie_and_didactiek_with_filters['results_total']['value']
        )

        # search with publish date filter applied
        search_biologie_upper_date = self.instance.search("biologie", filters=[
            {"external_id": self.datetime_field, "items": [None, "2018-12-31"]}
        ])
        self.assertTrue(search_biologie_upper_date["results"])
        for result in search_biologie_upper_date["results"]:
            self.assert_value_from_result(
                result,
                "published_at",
                date(year=2018, month=12, day=31),
                self.assertLessEqual
            )
        search_biologie_lower_date = self.instance.search("biologie", filters=[
            {"external_id": self.datetime_field, "items": ["2018-01-01", None]}
        ])
        self.assertTrue(search_biologie_lower_date["results"])
        for result in search_biologie_lower_date["results"]:
            self.assert_value_from_result(
                result,
                "published_at",
                datetime.strptime("2018-01-01", "%Y-%m-%d").date(),
                self.assertGreaterEqual
            )
        search_biologie_between_date = self.instance.search("biologie", filters=[
            {"external_id": self.datetime_field, "items": ["2018-01-01", "2018-12-31"]}
        ])
        self.assertTrue(search_biologie_between_date["results"])
        for result in search_biologie_between_date["results"]:
            self.assert_value_from_result(
                result,
                "published_at",
                datetime.strptime("2018-12-31", "%Y-%m-%d").date(),
                self.assertLessEqual
            )
            self.assert_value_from_result(
                result,
                "published_at",
                datetime.strptime("2018-01-01", "%Y-%m-%d").date(),
                self.assertGreaterEqual
            )

        # search with None, None as date filter. This search should give the same result as not filtering at all.
        search_biologie_none_date = self.instance.search("biologie", filters=[
            {"external_id": self.datetime_field, "items": [None, None]}
        ])
        search_biologie = self.instance.search("biologie")
        self.assertEqual(search_biologie_none_date, search_biologie)

    def test_aggregation_search(self):
        search_biologie = self.instance.search("biologie", drilldown_names=["technical_type"])
        self.assertIsNotNone(search_biologie)
        self.assertEqual(len(search_biologie[self.aggregation_key]), 2)
        for key, value in search_biologie[self.aggregation_key].items():
            self.assertIn("-", key)
            self.assertGreater(value, 0)

    def test_aggregation_with_filters(self):
        search = self.instance.search(
            "biologie",
            filters=[
                {"external_id": "technical_type", "items": ["document"]}
            ],
            drilldown_names=['harvest_source', 'technical_type']
        )

        aggregations = search[self.aggregation_key]

        total_for_technical_type = sum(
            count for name, count in aggregations.items() if "technical_type" in name
        )
        total_for_repo = sum(
            count for name, count in aggregations.items() if "harvest_source" in name
        )
        # The counts for format do not include the filter (as it is applied to format)
        # The counts for repo DO include the format filter, so it returns less results
        self.assertGreater(total_for_technical_type, total_for_repo)

    def test_ordering_search(self):
        # make a bunch of queries with different ordering
        search_biologie = self.instance.search("biologie")
        self.assertIsNotNone(search_biologie)
        self.assertTrue(search_biologie["results"])
        search_biologie_dates = [
            self.get_value_from_result(result, "published_at")
            for result in search_biologie["results"]
        ]
        search_biologie_asc = self.instance.search("biologie", ordering=self.datetime_field)
        self.assertIsNotNone(search_biologie_asc)
        self.assertTrue(search_biologie_asc["results"])
        search_biologie_asc_dates = [
            self.get_value_from_result(result, "published_at")
            for result in search_biologie_asc["results"]
        ]
        search_biologie_desc = self.instance.search("biologie", ordering=self.datetime_field)
        self.assertIsNotNone(search_biologie_desc)
        self.assertTrue(search_biologie_asc["results"])
        search_biologie_desc_dates = [
            self.get_value_from_result(result, "published_at")
            for result in search_biologie_desc["results"]
        ]
        # make sure that a default ordering is different than a date ordering
        self.assertNotEqual(search_biologie_dates, search_biologie_asc_dates)
        self.assertNotEqual(search_biologie_dates, search_biologie_desc_dates)
        # make sure that the dates of results are indeed in expected order
        self.assertEqual(search_biologie_asc_dates, sorted(search_biologie_asc_dates))
        self.assertEqual(search_biologie_desc_dates, sorted(search_biologie_desc_dates, reverse=False))

    def test_autocomplete(self):
        empty_autocomplete = self.instance.autocomplete(query='')
        self.assertEqual(len(empty_autocomplete), 0)
        biologie_autocomplete = self.instance.autocomplete(query='bio')
        self.assertGreater(len(biologie_autocomplete), 0)
        self.assertIsNot(empty_autocomplete, biologie_autocomplete)
        self.assertIsInstance(biologie_autocomplete, list)
        for item in biologie_autocomplete:
            self.assertIsInstance(item, str)
            self.assertTrue('biologie' in item)

    def test_drilldowns(self):
        empty_drilldowns = self.instance.drilldowns(drilldown_names=[])
        self.assertEqual(empty_drilldowns['results_total']['value'], 0)
        self.assertEqual(empty_drilldowns['results'], [])
        self.assertEqual(empty_drilldowns[self.aggregation_key], {})

        biologie_drilldowns = self.instance.drilldowns([], search_text="biologie")
        self.assertEqual(biologie_drilldowns['results_total']['value'], 0)
        self.assertEqual(biologie_drilldowns['results'], [])
        self.assertEqual(biologie_drilldowns[self.aggregation_key], {})

        repo_drilldowns = self.instance.drilldowns(['harvest_source'])
        for drilldown_name, value in repo_drilldowns[self.aggregation_key].items():
            self.assertIn("harvest_source", drilldown_name)
            self.assertGreater(value, 0)

        repo_and_format_drilldowns = self.instance.drilldowns(['harvest_source', 'technical_type'])
        for drilldown_name, value in repo_and_format_drilldowns[self.aggregation_key].items():
            field_id, external_id = drilldown_name.split("-")
            self.assertIn(field_id, ["harvest_source", "technical_type"])
            self.assertTrue(external_id)
            self.assertGreater(value, 0)

    def test_get_documents_by_id(self):
        # Sharekit product
        test_id = '3522b79c-928c-4249-a7f7-d2bcb3077f10'
        result = self.instance.get_documents_by_id(external_ids=[test_id])
        self.assertIsNotNone(result)
        self.assertEqual(result['results_total']['value'], 1, "Expected one result when searching for one id")
        document = result['results'][0]
        self.assertIsInstance(document, ResearchProduct)
        self.assertEqual(document.external_id, "3522b79c-928c-4249-a7f7-d2bcb3077f10")

    def test_get_documents_by_srn(self):
        test_id = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"  # factories don't change the platform
        result = self.instance.get_documents_by_srn([test_id])
        self.assertIsNotNone(result)
        self.assertEqual(result['results_total']['value'], 1, "Expected one result when searching for one id")
        document = result['results'][0]
        self.assertIsInstance(document, ResearchProduct)
        self.assertEqual(document.srn, test_id)

    def test_stats_integer(self):
        if not self.has_integer_stats:
            self.skipTest("TestCase isn't supporting integers as return type of stats.")
        stats = self.instance.stats()
        self.assertEqual(stats, 5)

    def test_stats_dict(self):
        if self.has_integer_stats:
            self.skipTest("TestCase isn't supporting dict as return type of stats.")
        stats = self.instance.stats()
        self.assertEqual(stats, {
            "documents": 5,
            "products": 5
        })

    def test_search_by_author(self):
        author = "Michel van Ast"
        expected_results_count = 5
        self.check_author_search(author, expected_results_count)

        author2 = "Theo van den Bogaart"
        expected_results_count2 = 2
        self.check_author_search(author2, expected_results_count2)

    def check_author_search(self, author, expected_results_count):
        search_author = self.instance.search(
            '',
            filters=[{"external_id": "authors.name.keyword", "items": [author]}]
        )
        for result in search_author['results']:
            authors = [author["name"] for author in self.get_value_from_result(result, 'authors')]
            self.assertIn(author, authors)
        self.assertEqual(search_author['results_total']['value'], expected_results_count)

    def test_search_did_you_mean(self):
        spelling_mistake = self.instance.search('didaktiek')
        self.assertIn("did_you_mean", spelling_mistake)
        self.assertEqual(spelling_mistake["did_you_mean"]["original"], "didaktiek")
        self.assertEqual(spelling_mistake["did_you_mean"]["suggestion"], "didactiek")
        no_result_spelling_mistake = self.instance.search('didaktiek is fantastiek')
        self.assertEqual(no_result_spelling_mistake["did_you_mean"], {})
        no_mistake = self.instance.search('biologie')
        self.assertEqual(no_mistake["did_you_mean"], {})
        unknown_mistake = self.instance.search('sdfkhjsdgaqegkjwfgklsd')
        self.assertEqual(unknown_mistake["did_you_mean"], {})

    def test_more_like_this(self):
        more_like_this = self.instance.more_like_this("surfsharekit:abc", "nl", is_external_identifier=False)
        self.assertEqual(more_like_this["results_total"]["value"], 4)
        self.assertEqual(more_like_this["results"][0].title, "Onderzoek over wiskundig denken")
        none_like_this = self.instance.more_like_this("surfsharekit:does-not-exist", "nl", is_external_identifier=False)
        self.assertEqual(none_like_this["results_total"]["value"], 0)
        self.assertEqual(none_like_this["results"], [])
        # Using external_id as input (legacy)
        legacy_like_this = self.instance.more_like_this("abc", "nl")
        self.assertEqual(legacy_like_this["results_total"]["value"], 4)
        self.assertEqual(legacy_like_this["results"][0].title, "Onderzoek over wiskundig denken")
        legacy_none_like_this = self.instance.more_like_this("does-not-exist", "nl")
        self.assertEqual(legacy_none_like_this["results_total"]["value"], 0)
        self.assertEqual(legacy_none_like_this["results"], [])

    def test_author_suggestions(self):
        author_expectation = "Theo van den Bogaart"
        suggestions = self.instance.author_suggestions(author_expectation)
        self.assertEqual(suggestions["results_total"]["value"], 3)
        for result in suggestions["results"]:
            author_names = [author["name"] for author in self.get_value_from_result(result, "authors")]
            self.assertNotIn(author_expectation, author_names)
            self.assertIn(author_expectation, result.description)

    def test_parse_search_hit(self):
        hit = {
            "_index": self.aliases[Entities.PRODUCTS],
            "_source": self.get_document_factory(Entities.PRODUCTS)(),
            "_score": 3.14,
            "highlight": {
                self.highlight_key: ["highlighted"]
            }
        }
        result = self.instance.parse_search_hit(hit)
        self.assertIsInstance(result, ResearchProduct)
        self.assertEqual(result.score, 3.14)
        self.assertEqual(result.highlight.text, ["highlighted"])
        self.assertIsNone(result.highlight.description)

    def test_parse_search_hit_minimal(self):
        hit = {
            "_index": self.aliases[Entities.PRODUCTS],
            "_source": self.get_document_factory(Entities.PRODUCTS)(),
        }
        result = self.instance.parse_search_hit(hit)
        self.assertIsInstance(result, ResearchProduct)
        self.assertEqual(result.score, 1.00)
        self.assertIsNone(result.highlight)

    def test_parse_search_hit_invalid_index(self):
        hit = {
            "_source": self.get_document_factory(Entities.PRODUCTS)(),
        }
        self.assertRaises(ValueError,  self.instance.parse_search_hit, [hit])


class TestResearchProductMultilingualIndicesSearchClient(TestResearchProductSearchClient):

    # Attributes used by SearchClientIntegrationTestCase
    platform = Platforms.PUBLINOVA
    presets = ["products:multilingual-indices"]

    # Attributes for test cases in this file
    aggregation_key = "drilldowns"
    datetime_field = "publisher_date"
    highlight_key = "text"
    has_integer_stats = True
