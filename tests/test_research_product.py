from dateutil.parser import parse
from datetime import datetime

from tests.base import BaseOpenSearchTestCase
from search_client import DocumentTypes
from search_client.factories import generate_nl_product


class TestResearchProductSearchClient(BaseOpenSearchTestCase):

    document_type = DocumentTypes.RESEARCH_PRODUCT

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.search.index(
            index=cls.get_alias("nl"),
            body=generate_nl_product(source="surfsharekit")
        )
        cls.search.index(
            id="abc",
            index=cls.get_alias("nl"),
            body=generate_nl_product(source="surfsharekit", external_id="abc",
                                     title="De wiskunde van Pythagoras", description="Groots is zijn onderzoek")
        )
        cls.search.index(
            index=cls.get_alias("nl"),
            body=generate_nl_product(source="surfsharekit", copyright="cc-by-40", topic="biology",
                                     publisher_date="2018-04-16T22:35:09+02:00"),
        )
        cls.search.index(
            index=cls.get_alias("nl"),
            body=generate_nl_product(source="surfsharekit", topic="biology",
                                     publisher_date="2019-04-16T22:35:09+02:00"),
        )
        cls.search.index(
            index=cls.get_alias("nl"),
            body=generate_nl_product(technical_type="video", source="surfsharekit", topic="biology"),
            refresh=True  # always put refresh on the last material
        )

    def get_value_from_record(self, record, key):
        if key == "authors":
            value = record["relations"]["authors"]
        elif key == "publishers":
            value = record["relations"]["parties"]
        elif key == "keywords":
            value = record["relations"]["keywords"]
        elif key == "technical_type":
            value = record["type"]
        elif key == "published_at":
            value = parse(record["published_at"], ignoretz=True)
        else:
            raise ValueError(f"No translation for key '{key}'")
        return value

    def assert_value_from_record(self, record, key, expectation, assertion=None, message=None):
        assertion = assertion or self.assertEqual
        if key == "publishers":
            expectation = [
                {"name": name}
                for name in expectation
            ]
        elif key == "keywords":
            expectation = [
                {"label": label}
                for label in expectation
            ]
        elif key == "studies":
            return  # silently skipping this assertion, because NPPO doesn't support studies
        value = self.get_value_from_record(record, key)
        assertion(value, expectation, message)

    def test_basic_search(self):
        search_result = self.instance.search('')
        search_result_filter = self.instance.search('', filters=[{"external_id": "technical_type", "items": ["video"]}])
        # did we get _anything_ from search?
        self.assertIsNotNone(search_result)
        self.assertIsNotNone(search_result_filter)
        self.assertGreater(search_result['recordcount'], search_result_filter['recordcount'])
        self.assertEqual(set(search_result.keys()), {"recordcount", "records", "drilldowns", "did_you_mean"})
        self.assertIsInstance(search_result['recordcount'], int)
        # does an empty search return a list of records?
        self.assertIsInstance(search_result['records'], list)
        # are there no drilldowns for an empty search?
        self.assertIsInstance(search_result['drilldowns'], dict)
        self.assertEqual(len(search_result['drilldowns']), 0)

        # basic search
        search_biologie = self.instance.search("biologie")
        self.assertIsNotNone(search_biologie)
        self.assertTrue(search_biologie["records"])
        self.assertIsNot(search_result, search_biologie)
        self.assertNotEqual(search_result['recordcount'], search_biologie['recordcount'])

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
        self.assertTrue(search_biologie_video["records"])
        for record in search_biologie_video["records"]:
            self.assert_value_from_record(record, "technical_type", "video")
        search_biologie_video_and_docs = self.instance.search(
            "biologie",
            filters=[{"external_id": "technical_type", "items": ["video", "document"]}]
        )
        self.assertGreater(len(search_biologie_video_and_docs["records"]), len(search_biologie_video["records"]))
        for record in search_biologie_video_and_docs["records"]:
            self.assert_value_from_record(record, "technical_type", ["video", "document"], self.assertIn)

        # search with multiple filters applied
        search_biologie_text_and_cc_by = self.instance.search(
            "biologie",
            filters=[
                {"external_id": "technical_type", "items": ["document"]},
                {"external_id": "copyright.keyword", "items": ["cc-by-40"]}
            ]
        )
        self.assertTrue(search_biologie_text_and_cc_by["records"])
        for record in search_biologie_text_and_cc_by["records"]:
            self.assert_value_from_record(record, "technical_type", "document")
            self.assertEqual(record["copyright"], "cc-by-40")

        # AND search with multiple filters applied
        search_biologie_and_didactiek = self.instance.search("biologie didactiek")
        search_biologie_and_didactiek_with_filters = self.instance.search(
            "biologie didactiek",
            filters=[
                {"external_id": "technical_type", "items": ["document"]},
                {"external_id": "copyright.keyword", "items": ["cc-by-40"]}
            ])

        self.assertIsNotNone(search_biologie_and_didactiek)
        self.assertTrue(search_biologie_and_didactiek["records"])
        self.assertIsNot(search_biologie_and_didactiek, search_biologie_and_didactiek_with_filters)
        self.assertTrue(search_biologie_and_didactiek_with_filters["records"])
        self.assertNotEqual(
            search_biologie_and_didactiek['recordcount'],
            search_biologie_and_didactiek_with_filters['recordcount']
        )

        # search with publish date filter applied
        search_biologie_upper_date = self.instance.search("biologie", filters=[
            {"external_id": "publisher_date", "items": [None, "2018-12-31"]}
        ])
        self.assertTrue(search_biologie_upper_date["records"])
        for record in search_biologie_upper_date["records"]:
            self.assert_value_from_record(
                record,
                "published_at",
                datetime(year=2018, month=12, day=31),
                self.assertLessEqual
            )
        search_biologie_lower_date = self.instance.search("biologie", filters=[
            {"external_id": "publisher_date", "items": ["2018-01-01", None]}
        ])
        self.assertTrue(search_biologie_lower_date["records"])
        for record in search_biologie_lower_date["records"]:
            self.assert_value_from_record(
                record,
                "published_at",
                datetime.strptime("2018-01-01", "%Y-%m-%d"),
                self.assertGreaterEqual
            )
        search_biologie_between_date = self.instance.search("biologie", filters=[
            {"external_id": "publisher_date", "items": ["2018-01-01", "2018-12-31"]}
        ])
        self.assertTrue(search_biologie_between_date["records"])
        for record in search_biologie_between_date["records"]:
            self.assert_value_from_record(
                record,
                "published_at",
                datetime.strptime("2018-12-31", "%Y-%m-%d"),
                self.assertLessEqual
            )
            self.assert_value_from_record(
                record,
                "published_at",
                datetime.strptime("2018-01-01", "%Y-%m-%d"),
                self.assertGreaterEqual
            )

        # search with None, None as date filter. This search should give the same result as not filtering at all.
        search_biologie_none_date = self.instance.search("biologie", filters=[
            {"external_id": "publisher_date", "items": [None, None]}
        ])
        search_biologie = self.instance.search("biologie")
        self.assertEqual(search_biologie_none_date, search_biologie)

    def test_drilldown_search(self):
        search_biologie = self.instance.search("biologie", drilldown_names=["technical_type"])
        self.assertIsNotNone(search_biologie)
        self.assertEqual(len(search_biologie['drilldowns']), 2)
        for key, value in search_biologie['drilldowns'].items():
            self.assertIn("-", key)
            self.assertGreater(value, 0)

    def test_drilldown_with_filters(self):
        search = self.instance.search(
            "biologie",
            filters=[
                {"external_id": "technical_type", "items": ["document"]}
            ],
            drilldown_names=['harvest_source', 'technical_type']
        )

        drilldowns = search['drilldowns']

        total_for_technical_type = sum(
            count for drilldown_name, count in drilldowns.items() if "technical_type" in drilldown_name
        )
        total_for_repo = sum(
            count for drilldown_name, count in drilldowns.items() if "harvest_source" in drilldown_name
        )
        # The counts for format do not include the filter (as it is applied to format)
        # The counts for repo DO include the format filter, so it returns less results
        self.assertGreater(total_for_technical_type, total_for_repo)

    def test_ordering_search(self):
        # make a bunch of queries with different ordering
        search_biologie = self.instance.search("biologie")
        self.assertIsNotNone(search_biologie)
        self.assertTrue(search_biologie["records"])
        search_biologie_dates = [
            self.get_value_from_record(record, "published_at")
            for record in search_biologie["records"]
        ]
        search_biologie_asc = self.instance.search("biologie", ordering="publisher_date")
        self.assertIsNotNone(search_biologie_asc)
        self.assertTrue(search_biologie_asc["records"])
        search_biologie_asc_dates = [
            self.get_value_from_record(record, "published_at")
            for record in search_biologie_asc["records"]
        ]
        search_biologie_desc = self.instance.search("biologie", ordering="publisher_date")
        self.assertIsNotNone(search_biologie_desc)
        self.assertTrue(search_biologie_asc["records"])
        search_biologie_desc_dates = [
            self.get_value_from_record(record, "published_at")
            for record in search_biologie_desc["records"]
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
        self.assertGreater(empty_drilldowns['recordcount'], 0)
        self.assertEqual(empty_drilldowns['records'], [])
        self.assertEqual(empty_drilldowns['drilldowns'], {})

        biologie_drilldowns = self.instance.drilldowns([], search_text="biologie")
        self.assertGreater(biologie_drilldowns['recordcount'], 0)
        self.assertGreater(empty_drilldowns['recordcount'], biologie_drilldowns['recordcount'])
        self.assertEqual(empty_drilldowns['records'], [])
        self.assertEqual(empty_drilldowns['drilldowns'], {})

        repo_drilldowns = self.instance.drilldowns(['harvest_source'])
        for drilldown_name, value in repo_drilldowns['drilldowns'].items():
            self.assertIn("harvest_source", drilldown_name)
            self.assertGreater(value, 0)

        repo_and_format_drilldowns = self.instance.drilldowns(['harvest_source', 'technical_type'])
        for drilldown_name, value in repo_and_format_drilldowns['drilldowns'].items():
            field_id, external_id = drilldown_name.split("-")
            self.assertIn(field_id, ["harvest_source", "technical_type"])
            self.assertTrue(external_id)
            self.assertGreater(value, 0)

    def test_get_materials_by_id(self):
        # Sharekit material
        test_id = '3522b79c-928c-4249-a7f7-d2bcb3077f10'
        result = self.instance.get_materials_by_id(external_ids=[test_id])
        self.assertIsNotNone(result)
        self.assertEqual(result['recordcount'], 1, "Expected one result when searching for one id")
        material = result['records'][0]

        self.assertEqual(material['title'], 'Onderzoek over wiskundig denken')
        self.assertEqual(
            material['url'],
            "https://maken.wikiwijs.nl/91192/Wiskundedidactiek_en_ICT"
        )
        self.assertEqual(material['external_id'], "3522b79c-928c-4249-a7f7-d2bcb3077f10")
        self.assert_value_from_record(material, 'publishers', ["Wikiwijs Maken"])
        self.assert_value_from_record(
            material,
            'published_at',
            datetime(year=2017, month=4, day=16, hour=22, minute=35, second=9)
        )
        self.assert_value_from_record(material, 'authors', [
            {"name": "Michel van Ast"},
            {"name": "Theo van den Bogaart"},
            {"name": "Marc de Graaf"},
        ])
        self.assert_value_from_record(material, 'keywords', ["nerds"])
        self.assert_value_from_record(material, 'studies', [
            "7afbb7a6-c29b-425c-9c59-6f79c845f5f0",  # math
            "0861c43d-1874-4788-b522-df8be575677f"  # onderwijskunde
        ])
        self.assertEqual(material['language'], 'nl')
        self.assert_value_from_record(material, 'technical_type', 'document')

        # Sharekit
        test_id = '3522b79c-928c-4249-a7f7-d2bcb3077f10'
        result = self.instance.get_materials_by_id(external_ids=[test_id])
        self.assertIsNotNone(result)
        self.assertEqual(result['recordcount'], 1, "Expected one result when searching for one id")
        material = result['records'][0]
        self.assertEqual(material['external_id'], "3522b79c-928c-4249-a7f7-d2bcb3077f10")

    def test_search_by_author(self):
        author = "Michel van Ast"
        expected_record_count = 5
        self.check_author_search(author, expected_record_count)

        author2 = "Theo van den Bogaart"
        expected_record_count2 = 2
        self.check_author_search(author2, expected_record_count2)

    def check_author_search(self, author, expected_record_count):
        search_author = self.instance.search(
            '',
            filters=[{"external_id": "authors.name.keyword", "items": [author]}]
        )
        for record in search_author['records']:
            authors = [author["name"] for author in self.get_value_from_record(record, 'authors')]
            self.assertIn(author, authors)
        self.assertEqual(search_author['recordcount'], expected_record_count)

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
        more_like_this = self.instance.more_like_this("abc", "nl")
        self.assertEqual(more_like_this["records_total"], 4)
        self.assertEqual(more_like_this["results"][0]["title"], "Onderzoek over wiskundig denken")
        none_like_this = self.instance.more_like_this("does-not-exist", "nl")
        self.assertEqual(none_like_this["records_total"], 0)
        self.assertEqual(none_like_this["results"], [])

    def test_author_suggestions(self):
        suggestions = self.instance.author_suggestions("Theo")
        author_expectation = "Theo van den Bogaart"
        self.assertEqual(suggestions["records_total"], 3)
        for result in suggestions["results"]:
            author_names = [author["name"] for author in self.get_value_from_record(result, "authors")]
            self.assertNotIn(author_expectation, author_names)
            self.assertIn(author_expectation, result["description"])

    def test_parse_search_hit(self):
        authors = [{"name": "author"}]
        hit = {
            "_source": {
                "title": "title",
                "description": "description",
                "authors": authors,
                "learning_material_disciplines_normalized": ["discipline"],
                "research_themes": ["theme"]
            }
        }
        record = self.instance.parse_search_hit(hit)
        self.assertIn("relations", record, "Expected research products record to have a relations key")
        self.assertNotIn("authors", record, "Expected authors to be absent in main record for tr")
        self.assertNotIn("themes", record, "Expected themes to be absent in main record for research products")
        self.assertIn("authors", record["relations"], "Expected authors to be part of relations for research products")
        self.assertIn("themes", record["relations"], "Expected themes to be part of relations for research products")
        self.assertEqual(record["title"], "title")
        self.assertEqual(record["description"], "description")
        self.assertEqual(record["relations"]["authors"], authors)
        self.assertEqual(record["relations"]["themes"], [{"label": "theme"}])
        self.assertEqual(
            record["relations"]["keywords"], [],
            "Expected data not given in research products to have a default"
        )
        self.assertEqual(
            record["relations"]["parents"], [],
            "Expected data not given in research products to have a default"
        )
        self.assertEqual(
            record["relations"]["children"], [],
            "Expected data not given in research products to have a default"
        )
        # Checking an edge case where keywords may be None
        hit["_source"]["keywords"] = None
        record = self.instance.parse_search_hit(hit)
        self.assertEqual(record["relations"]["keywords"], [])
