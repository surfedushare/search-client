from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from django.db import connection
from django.conf import settings

from elasticsearch import Elasticsearch


class BaseTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1920,1080")

        cls.selenium = WebDriver(options=chrome_options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        # FIXME: Ugly hack to kill open connections. Somehow it doesn't work on Github Actions otherwise.
        # There seems to be a running query for the filter tree which doesn't terminate in time.
        with connection.cursor() as c:
            c.execute("SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'test_edushare' AND pid <> pg_backend_pid();")

class ElasticSearchTestCase(BaseTestCase):
    @classmethod
    def index_body(cls, language):
        # TODO: Share config with harvester somehow
        analyzer = 'dutch' if language == 'nl' else 'english'
        return {
            "mappings": {
                "_doc": {
                    "properties": {
                        'title': {
                            'type': 'text',
                            'analyzer': analyzer
                        },
                        'text': {
                            'type': 'text',
                            'analyzer': analyzer
                        },
                        'transcription': {
                            'type': 'text',
                            'analyzer': analyzer
                        },
                        'description': {
                            'type': 'text',
                            'analyzer': analyzer
                        },
                        'url': {'type': 'text'},
                        'title_plain': {'type': 'text'},
                        'text_plain': {'type': 'text'},
                        'transcription_plain': {'type': 'text'},
                        'description_plain': {'type': 'text'},
                        'author': {
                            'type': 'keyword'
                        },
                        'keywords': {
                            'type': 'keyword'
                        },
                        'file_type': {
                            'type': 'keyword'
                        },
                        'id': {'type': 'text'},
                        'external_id': {
                            'type': 'keyword'
                        },
                        'arrangement_collection_name': {
                            'type': 'keyword'
                        },
                        'educational_levels': {
                            'type': 'keyword'
                        },
                        'lom_educational_levels': {
                            'type': 'keyword'
                        },
                        'disciplines': {
                            'type': 'keyword'
                        },
                        "suggest" : {
                            "type" : "completion"
                        },
                    }
                }
            }
        }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.elastic = Elasticsearch(
            [settings.ELASTICSEARCH_HOST],
            http_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
        )
        cls.elastic.indices.create(settings.ELASTICSEARCH_NL_INDEX, ignore=400, body=cls.index_body('nl'))
        cls.elastic.indices.create(settings.ELASTICSEARCH_EN_INDEX, ignore=400, body=cls.index_body('en'))

    @classmethod
    def tearDownClass(cls):
        cls.elastic.indices.delete(settings.ELASTICSEARCH_NL_INDEX)
        cls.elastic.indices.delete(settings.ELASTICSEARCH_EN_INDEX)
