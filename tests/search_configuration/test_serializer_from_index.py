from pydantic import BaseModel

from search_client.constants import Platforms
from tests.base import SearchClientTestCase


class TestSerializerFromIndex(SearchClientTestCase):
    """
    The integration tests cover working with indices that have prefixes to
    keep local production copies intact when testing.
    However we do need to cover a bit more logic around index selection with indices we also see in production.
    This TestCase provides these test.
    """
    platform = Platforms.PUBLINOVA
    presets = ["products:default", "projects:default"]

    def test_get_serializer_from_index(self):
        test_indices = [
            "publinova-products--epsilon-100",  # Dataset=epsilon and Harvester code_version=1.0.0
            "publinova-products",  # this is actually an alias
            "publinova-projects--epsilon-100",  # Dataset=epsilon and Harvester code_version=1.0.0
            "publinova-projects"  # this is actually an alias
        ]
        retrieved_serializers = []
        for test_index in test_indices:
            serializer = self.instance.configuration.get_serializer_from_index(test_index)
            self.assertTrue(issubclass(serializer, BaseModel))
            retrieved_serializers.append(serializer.__qualname__)
        self.assertEqual(retrieved_serializers, ["ResearchProduct", "ResearchProduct", "Project", "Project"])
