import os
from unittest import TestCase

from configuration import create_configuration

from search_client.opensearch import SearchClient, OpenSearchClientBuilder
from search_client.constants import DocumentTypes, LANGUAGES, Platforms
from search_client.opensearch.indices.legacy import create_open_search_index_configuration


class BaseOpenSearchTestCase(TestCase):

    instance = None
    search = None
    config = None
    platform = Platforms.EDUSOURCES

    @classmethod
    def index_body(cls, language):
        return create_open_search_index_configuration(language, DocumentTypes.LEARNING_MATERIAL)

    @classmethod
    def get_alias(cls, language):
        return f"{cls.platform.value}-{language}"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.config = create_configuration(project_location=project_location)
        cls.search = OpenSearchClientBuilder.from_host(cls.config.open_search.url).build()
        for language in LANGUAGES:
            cls.search.indices.create(
                cls.get_alias(language),
                ignore=400,
                body=cls.index_body(language)
            )
        cls.instance = SearchClient(cls.search, cls.platform)

    @classmethod
    def tearDownClass(cls):
        for language in LANGUAGES:
            cls.search.indices.delete(
                cls.get_alias(language)
            )
        cls.search.close()
        cls.instance.client.close()
        super().tearDownClass()
