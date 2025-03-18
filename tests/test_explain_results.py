from tests.base import SearchClientIntegrationTestCase
from search_client.constants import Platforms, Entities
from search_client.exceptions import ResultNotFound


class TestResearchProductExplain(SearchClientIntegrationTestCase):

    # Attributes used by SearchClientIntegrationTestCase
    platform = Platforms.PUBLINOVA
    presets = ["products:default"]

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

    def test_explain_result_math(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 4.37734,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.87547,
                        "texts.nl.titles.text.analyzed": 1.75094
                    },
                    "score": 2.62641,
                    "relevancy": 0.6
                },

                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text": 0.87547,
                        "texts.nl.contents.text.folded": 0.87547
                    },
                    "score": 1.75094,
                    "relevancy": 0.4
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_math_research(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde onderzoek")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 5.42148,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.87547,
                        "texts.nl.titles.text.analyzed": 1.75094
                    },
                    "score": 2.62641,
                    "relevancy": 0.48
                },
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text": 0.87547,
                        "texts.nl.contents.text.folded": 0.87547
                    },
                    "score": 1.75094,
                    "relevancy": 0.32
                },
                {
                    "term": "onderzoek",
                    "fields": {
                        "texts.nl.contents.text": 0.08701,
                        "texts.nl.contents.text.analyzed": 0.08701,
                        "texts.nl.contents.text.folded": 0.08701,
                        "texts.nl.descriptions.text": 0.08701,
                        "texts.nl.descriptions.text.analyzed": 0.08701,
                        "texts.nl.descriptions.text.folded": 0.08701,
                        "texts.nl.titles.text": 0.17402,
                        "texts.nl.titles.text.analyzed": 0.17402,
                        "texts.nl.titles.text.folded": 0.17402,
                    },
                    "score": 1.04412,
                    "relevancy": 0.19
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_biology(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "surfsharekit:def",
            "total_score": 1.61699,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.539,
                        "texts.nl.contents.text.analyzed": 0.539,
                        "texts.nl.contents.text": 0.539
                    },
                    "score": 1.617,
                    "relevancy": 1.0
                }
            ],
            "recency_bonus": 0.04594
        })

    def test_explain_result_biology_research(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie onderzoek")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "surfsharekit:def",
            "total_score": 2.66113,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.539,
                        "texts.nl.contents.text.analyzed": 0.539,
                        "texts.nl.contents.text": 0.539
                    },
                    "score": 1.617,
                    "relevancy": 0.61
                },
                {
                    "term": "onderzoek",
                    "fields": {
                        "texts.nl.descriptions.text": 0.08701,
                        "texts.nl.contents.text.folded": 0.08701,
                        "texts.nl.titles.text": 0.17402,
                        "texts.nl.descriptions.text.folded": 0.08701,
                        "texts.nl.contents.text.analyzed": 0.08701,
                        "texts.nl.descriptions.text.analyzed": 0.08701,
                        "texts.nl.contents.text": 0.08701,
                        "texts.nl.titles.text.analyzed": 0.17402,
                        "texts.nl.titles.text.folded": 0.17402
                    },
                    "score": 1.04412,
                    "relevancy": 0.39
                }
            ],
            "recency_bonus": 0.04594
        })

    def test_explain_result_no_search(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "")

    def test_explain_result_not_found(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "not-found")


class TestLearningMaterialSearchClient(SearchClientIntegrationTestCase):

    # Attributes used by SearchClientIntegrationTestCase
    platform = Platforms.EDUSOURCES
    presets = ["products:default"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.index_document(Entities.PRODUCTS, educational_levels=["HBO"], source="surfsharekit")
        cls.index_document(
            Entities.PRODUCTS,
            educational_levels=["HBO"], source="surfsharekit", external_id="abc",
            title="De wiskunde van Pythagoras", description="Groots zijn zijn getallen"
        )
        cls.index_document(
            Entities.PRODUCTS,
            educational_levels=["HBO"], source="surfsharekit", copyright="cc-by-40", topic="biology",
            publisher_date="2018-04-16T22:35:09+02:00"
        )
        cls.index_document(
            Entities.PRODUCTS,
            educational_levels=["HBO"], source="edurep", topic="biology",
            external_id="WikiwijsDelen:urn:uuid:abc", publisher_date="2019-04-16T22:35:09+02:00"
        )
        cls.index_document(
            Entities.PRODUCTS, is_last_entity_document=True,
            educational_levels=["HBO"], technical_type="video", source="surfsharekit", topic="biology",
            external_id="def"
        )

    def test_explain_result_math(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 4.37734,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.87547,
                        "texts.nl.titles.text.analyzed": 1.75094
                    },
                    "score": 2.62641,
                    "relevancy": 0.6
                },

                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text": 0.87547,
                        "texts.nl.contents.text.folded": 0.87547
                    },
                    "score": 1.75094,
                    "relevancy": 0.4
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_math_didactic(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde didactiek")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 5.16045,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.87547,
                        "texts.nl.titles.text.analyzed": 1.75094
                    },
                    "score": 2.62641,
                    "relevancy": 0.51
                },
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.87547,
                        "texts.nl.contents.text": 0.87547
                    },
                    "score": 1.75094,
                    "relevancy": 0.34
                },
                {
                    "term": "didactiek",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.08701,
                        "texts.nl.titles.text": 0.17402,
                        "texts.nl.contents.text.analyzed": 0.08701,
                        "texts.nl.contents.text": 0.08701,
                        "texts.nl.titles.text.analyzed": 0.17402,
                        "texts.nl.titles.text.folded": 0.17402
                    },
                    "score": 0.78309,
                    "relevancy": 0.15
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_biology(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "surfsharekit:def",
            "total_score": 1.61699,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.539,
                        "texts.nl.contents.text.analyzed": 0.539,
                        "texts.nl.contents.text": 0.539
                    },
                    "score": 1.617,
                    "relevancy": 1.0
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_biology_didactic(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie didactiek")
        self.assertEqual(explain_result.model_dump(mode="json"), {
            "srn": "surfsharekit:def",
            "total_score": 2.40009,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.539,
                        "texts.nl.contents.text.analyzed": 0.539,
                        "texts.nl.contents.text": 0.539
                    },
                    "score": 1.617,
                    "relevancy": 0.67
                },
                {
                    "term": "didactiek",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.08701,
                        "texts.nl.titles.text": 0.17402,
                        "texts.nl.contents.text.analyzed": 0.08701,
                        "texts.nl.contents.text": 0.08701,
                        "texts.nl.titles.text.analyzed": 0.17402,
                        "texts.nl.titles.text.folded": 0.17402
                    },
                    "score": 0.78309,
                    "relevancy": 0.33
                }
            ],
            "recency_bonus": 0.0347
        })

    def test_explain_result_no_search(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "")

    def test_explain_result_not_found(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "not-found")
