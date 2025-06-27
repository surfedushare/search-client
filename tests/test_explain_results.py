from unittest import TestCase

from tests.base import SearchClientIntegrationTestCase
from search_client.constants import Platforms, Entities
from search_client.exceptions import ResultNotFound
from search_client.serializers.core import SearchTermExplanation


def round_scores(explanation_dump: dict) -> dict:
    for key, value in explanation_dump.items():
        if isinstance(value, float):
            explanation_dump[key] = round(value, 2)
        elif key == "terms":
            for term in explanation_dump["terms"]:
                for term_key, term_value in term.items():
                    if isinstance(term_value, float):
                        term[term_key] = round(term_value, 2)
                for field_key, field_value in term["fields"].items():
                    if isinstance(field_value, float):
                        term["fields"][field_key] = round(field_value, 2)
    return explanation_dump


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
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        recency_bonus = explain_result_dump.pop("recency_bonus")
        self.assertIsInstance(
            recency_bonus, float,
            "Expected recency bonus to change over time, but always be a float."
        )
        self.assertEqual(explain_result_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 4.33,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.88,
                        "texts.nl.titles.text.analyzed": 1.7
                    },
                    "score": 2.58,
                    "relevancy": 0.6
                },
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.88,
                        "texts.nl.contents.text": 0.88
                    },
                    "score": 1.75,
                    "relevancy": 0.4
                }
            ]
        })

    def test_explain_result_math_research(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde onderzoek")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        recency_bonus = explain_result_dump.pop("recency_bonus")
        self.assertIsInstance(
            recency_bonus, float,
            "Expected recency bonus to change over time, but always be a float."
        )
        self.assertEqual(explain_result_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 6.54,
            "terms": [
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.88,
                        "texts.nl.titles.text.analyzed": 1.7
                    },
                    "score": 2.58,
                    "relevancy": 0.39
                },
                {
                    "term": "onderzoek",
                    "fields": {
                        "texts.nl.descriptions.text": 0.08,
                        "texts.nl.contents.text.folded": 0.09,
                        "texts.nl.titles.text": 0.58,
                        "texts.nl.descriptions.text.folded": 0.08,
                        "texts.nl.contents.text.analyzed": 0.09,
                        "texts.nl.descriptions.text.analyzed": 0.08,
                        "texts.nl.contents.text": 0.09,
                        "texts.nl.titles.text.analyzed": 0.56,
                        "texts.nl.titles.text.folded": 0.58
                    },
                    "score": 2.21,
                    "relevancy": 0.34
                },
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.88,
                        "texts.nl.contents.text": 0.88
                    },
                    "score": 1.75,
                    "relevancy": 0.27
                }
            ]
        })

    def test_explain_result_biology(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        recency_bonus = explain_result_dump.pop("recency_bonus")
        self.assertIsInstance(
            recency_bonus, float,
            "Expected recency bonus to change over time, but always be a float."
        )
        self.assertEqual(explain_result_dump, {
            "srn": "surfsharekit:def",
            "total_score": 1.62,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.54,
                        "texts.nl.contents.text.analyzed": 0.54,
                        "texts.nl.contents.text": 0.54
                    },
                    "score": 1.62,
                    "relevancy": 1.0
                }
            ]
        })

    def test_explain_result_biology_research(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie onderzoek")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        recency_bonus = explain_result_dump.pop("recency_bonus")
        self.assertIsInstance(
            recency_bonus, float,
            "Expected recency bonus to change over time, but always be a float."
        )
        self.assertEqual(explain_result_dump, {
            "srn": "surfsharekit:def",
            "total_score": 3.83,
            "terms": [
                {
                    "term": "onderzoek",
                    "fields": {
                        "texts.nl.descriptions.text": 0.08,
                        "texts.nl.contents.text.folded": 0.09,
                        "texts.nl.titles.text": 0.58,
                        "texts.nl.descriptions.text.folded": 0.08,
                        "texts.nl.contents.text.analyzed": 0.09,
                        "texts.nl.descriptions.text.analyzed": 0.08,
                        "texts.nl.contents.text": 0.09,
                        "texts.nl.titles.text.analyzed": 0.56,
                        "texts.nl.titles.text.folded": 0.58
                    },
                    "score": 2.21,
                    "relevancy": 0.58
                },
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.54,
                        "texts.nl.contents.text.analyzed": 0.54,
                        "texts.nl.contents.text": 0.54
                    },
                    "score": 1.62,
                    "relevancy": 0.42
                }
            ]
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
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        self.assertEqual(explain_result_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 6.98,
            "terms": [
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text.folded": 2.63,
                        "texts.nl.contents.text": 2.63
                    },
                    "score": 5.25,
                    "relevancy": 0.75
                },
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.88,
                        "texts.nl.titles.text.analyzed": 0.85
                    },
                    "score": 1.73,
                    "relevancy": 0.25
                }
            ],
            "recency_bonus": 0.03
        })

    def test_explain_result_math_didactic(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        explain_result = self.instance.explain_result(identifier, "wiskunde didactiek")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        self.assertEqual(explain_result_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "total_score": 10.74,
            "terms": [
                {
                    "term": "wiskunde",
                    "fields": {
                        "texts.nl.contents.text.folded": 2.63,
                        "texts.nl.contents.text": 2.63
                    },
                    "score": 5.25,
                    "relevancy": 0.49
                },
                {
                    "term": "didactiek",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.26,
                        "texts.nl.titles.text": 1.44,
                        "texts.nl.contents.text.analyzed": 0.09,
                        "texts.nl.contents.text": 0.26,
                        "texts.nl.titles.text.analyzed": 0.28,
                        "texts.nl.titles.text.folded": 1.44
                    },
                    "score": 3.77,
                    "relevancy": 0.35
                },
                {
                    "term": "wiskund",
                    "fields": {
                        "texts.nl.contents.text.analyzed": 0.88,
                        "texts.nl.titles.text.analyzed": 0.85
                    },
                    "score": 1.73,
                    "relevancy": 0.16
                }
            ],
            "recency_bonus": 0.03
        })

    def test_explain_result_biology(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        self.assertEqual(explain_result_dump, {
            "srn": "surfsharekit:def",
            "total_score": 3.77,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 1.62,
                        "texts.nl.contents.text.analyzed": 0.54,
                        "texts.nl.contents.text": 1.62
                    },
                    "score": 3.77,
                    "relevancy": 1.0
                }
            ],
            "recency_bonus": 0.03
        })

    def test_explain_result_biology_didactic(self):
        identifier = "surfsharekit:def"
        explain_result = self.instance.explain_result(identifier, "biologie didactiek")
        explain_result_dump = round_scores(explain_result.model_dump(mode="json"))
        self.assertEqual(explain_result_dump, {
            "srn": "surfsharekit:def",
            "total_score": 7.54,
            "terms": [
                {
                    "term": "biologie",
                    "fields": {
                        "texts.nl.contents.text.folded": 1.62,
                        "texts.nl.contents.text.analyzed": 0.54,
                        "texts.nl.contents.text": 1.62
                    },
                    "score": 3.77,
                    "relevancy": 0.5
                },
                {
                    "term": "didactiek",
                    "fields": {
                        "texts.nl.contents.text.folded": 0.26,
                        "texts.nl.titles.text": 1.44,
                        "texts.nl.contents.text.analyzed": 0.09,
                        "texts.nl.contents.text": 0.26,
                        "texts.nl.titles.text.analyzed": 0.28,
                        "texts.nl.titles.text.folded": 1.44
                    },
                    "score": 3.77,
                    "relevancy": 0.5
                }
            ],
            "recency_bonus": 0.03
        })

    def test_explain_result_no_search(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "")

    def test_explain_result_not_found(self):
        identifier = "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
        with self.assertRaises(ResultNotFound):
            self.instance.explain_result(identifier, "not-found")


class TestSearchTermExplanation(TestCase):

    explanation_descriptions = [
        "weight(Synonym(texts.nl.contents.text.analyzed:gevende texts.nl.contents.text.analyzed:leiding texts.nl.contents.text.analyzed:leidinggevende) in 574) [PerFieldSimilarity], result of:",  # noqa: E501
        "weight(texts.nl.descriptions.text.folded:leidinggevende in 574) [PerFieldSimilarity], result of:"
    ]
    expected_fields = [
        "texts.nl.contents.text.analyzed",
        "texts.nl.descriptions.text.folded",
    ]
    expected_terms = [
        "gevende | leiding | leidinggevende",
        "leidinggevende",
    ]

    def test_parse_explanation_description(self):
        for ix, test_description in enumerate(self.explanation_descriptions):
            field, term = SearchTermExplanation.parse_explanation_description(test_description)
            self.assertEqual(term, self.expected_terms[ix])
            self.assertEqual(field, self.expected_fields[ix])

    def test_parse_explanation_descriptions_no_match(self):
        self.assertRaises(ValueError, SearchTermExplanation.parse_explanation_description, "")
        self.assertRaises(ValueError, SearchTermExplanation.parse_explanation_description, "sum of:")
