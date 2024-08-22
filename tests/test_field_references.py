from unittest import TestCase

from search_client.constants import Platforms
from search_client.opensearch.configuration import get_preset_search_configuration


class TestFieldReferences(TestCase):

    def test_interpolating_default_references(self):
        configuration = get_preset_search_configuration(Platforms.EDUSOURCES, "products:default")
        fields = configuration.interpolate_field_languages(
            "texts:titles", "texts:descriptions", "texts.nl.contents.text", "publishers"
        )
        self.assertEqual(fields, [
            "texts.nl.titles.text", "texts.en.titles.text", "texts.unk.titles.text",
            "texts.nl.descriptions.text", "texts.en.descriptions.text", "texts.unk.descriptions.text",
            "texts.nl.contents.text", "publishers"
        ])

    def test_extrapolating_default_fields(self):
        configuration = get_preset_search_configuration(Platforms.EDUSOURCES, "products:default")
        references = configuration.extrapolate_field_references(
            "texts.nl.titles.text", "texts.nl.contents.text","texts.en.descriptions.text", "texts.unk.contents.text",
            "texts.unk.descriptions.text", "publishers"
        )
        self.assertEqual(references, ["publishers", "texts:contents", "texts:descriptions", "texts:titles"])

    def test_interpolating_multilingual_indices_fields(self):
        configuration = get_preset_search_configuration(Platforms.EDUSOURCES, "products:multilingual-indices")
        fields = configuration.interpolate_field_languages("title", "description", "text", "publishers")
        self.assertEqual(fields, ["title", "description", "text", "publishers"])

    def test_extrapolating_multilingual_indices_fields(self):
        configuration = get_preset_search_configuration(Platforms.EDUSOURCES, "products:multilingual-indices")
        references = configuration.extrapolate_field_references("title", "description", "text", "publishers")
        self.assertEqual(references, ["description", "publishers", "text", "title"])
