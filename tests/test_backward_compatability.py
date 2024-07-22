from tests.base import BaseOpenSearchTestCase


class TestCleaningLegacyExternalIdPrefixes(BaseOpenSearchTestCase):

    def test_legacy_external_id_prefixes(self):
        self.assertEqual(
            self.instance.clean_external_id("edurep_delen:abc"), "WikiwijsDelen:urn:uuid:abc",
            "Expected edurep_delen prefix to get replaced"
        )
        self.assertEqual(self.instance.clean_external_id("abc"), "abc", "Expected Sharekit prefixes to be left alone")
        self.assertEqual(
            self.instance.clean_external_id("surf:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("surfsharekit:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("oer_han:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )
