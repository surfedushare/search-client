import os
from unittest import TestCase

from opensearchpy import OpenSearch

from configuration import create_configuration
from search_client.constants import Platforms
from search_client.opensearch.client import SearchClient, OpenSearchClientBuilder
from search_client.test.cases import SearchClientIntegrationTestCaseMixin


class SearchClientIntegrationTestCase(SearchClientIntegrationTestCaseMixin, TestCase):

    @classmethod
    def setup_opensearch_client(cls) -> OpenSearch:
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = create_configuration(project_location=project_location)
        return OpenSearchClientBuilder.from_host(config.open_search.url).build()


class SearchClientTestCase(TestCase):
    """
    A base test case to unittest methods on the SearchClient that don't require functional indices.
    """

    instance = None
    platform = Platforms.EDUSOURCES
    presets = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config = create_configuration(project_location=project_location)
        opensearch_client = OpenSearchClientBuilder.from_host(config.open_search.url).build()
        cls.instance = SearchClient(opensearch_client, cls.platform, presets=cls.presets)
