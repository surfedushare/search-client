import os
from unittest import TestCase
from opensearchpy import OpenSearch

from configuration import create_configuration

from search_client import SearchClient
from search_client.constants import DocumentTypes, LANGUAGES
from search_client.opensearch.configuration import create_open_search_index_configuration


class BaseOpenSearchTestCase(TestCase):

    instance = None
    document_type = None
    search = None
    config = None

    @classmethod
    def index_body(cls, language):
        return create_open_search_index_configuration(language, DocumentTypes.LEARNING_MATERIAL)

    @classmethod
    def get_alias(cls, language):
        return f"{cls.config.open_search.alias_prefix}-{language}"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        project_location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.config = create_configuration(project_location=project_location)
        cls.search = OpenSearch(
            [cls.config.open_search.url]
        )
        for language in LANGUAGES:
            cls.search.indices.create(
                cls.get_alias(language),
                ignore=400,
                body=cls.index_body('nl')
            )
        cls.instance = SearchClient(
            cls.config.open_search.url,
            cls.document_type,
            cls.config.open_search.alias_prefix,
            search_results_key="results"
        )

    @classmethod
    def tearDownClass(cls):
        for language in LANGUAGES:
            cls.search.indices.delete(
                cls.get_alias(language)
            )
        cls.search.close()
        cls.instance.client.close()
        super().tearDownClass()
