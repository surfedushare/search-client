from unittest import TestCase

from search_client.constants import Platforms
from search_client.opensearch.configuration import (SearchConfiguration, is_valid_preset_search_configuration,
                                                    get_preset_search_configuration)


class TestIsValidPresetSearchConfiguration(TestCase):

    def test_valid_preset(self):
        for platform in Platforms:
            preset = is_valid_preset_search_configuration(platform, "products:default")
            self.assertEqual(preset, "products:default")

    def test_valid_missing_subtype(self):
        for platform in Platforms:
            preset = is_valid_preset_search_configuration(platform, "products")
            self.assertEqual(preset, "products:default")

    def test_invalid_entity(self):
        for platform in Platforms:
            self.assertRaises(ValueError, is_valid_preset_search_configuration, platform, "unknown:default")

    def test_invalid_entity_missing_subtype(self):
        for platform in Platforms:
            self.assertRaises(ValueError, is_valid_preset_search_configuration, platform, "unknown")

    def test_get_configuration_default(self):
        for platform in Platforms:
            configuration = get_preset_search_configuration(platform, "products:default")
            self.assertIsInstance(configuration, SearchConfiguration)

    def test_get_configuration_missing_subtype(self):
        for platform in Platforms:
            configuration = get_preset_search_configuration(platform, "products")
            self.assertIsInstance(configuration, SearchConfiguration)

    def test_get_configuration_invalid_entity(self):
        for platform in Platforms:
            self.assertRaises(ValueError, get_preset_search_configuration, platform, "unknown:default")

    def test_get_configuration_invalid_entity_missing_subtype(self):
        for platform in Platforms:
            self.assertRaises(ValueError, get_preset_search_configuration, platform, "unknown")
