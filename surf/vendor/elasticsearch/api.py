from elasticsearch import Elasticsearch

index_nl = 'gamma-nl-12'
index_en = 'gamma-en-13'


class ElasticSearchApiClient:
    def __init__(self):
        self.elastic = Elasticsearch(
            ['elastic.surfpol.nl'],
            http_auth=('search', 'Kbd5FMH8EF0gEuxgnNeNJmUBBBtc'),
            scheme="https",
            port=443,
        )

    def autocomplete(self, query):
        query_dictionary = {
            'suggest': {
                "autocomplete": {
                    'text': query,
                    "completion": {
                        "field": "suggest"
                    }
                }
            }
        }

        result = self.elastic.search(
            index=index,
            doc_type='entity',
            body=query_dictionary,
            _source_include='suggest'
        )

        autocomplete = result['suggest']['autocomplete']
        options = autocomplete[0]['options']
        flat_options = list(set([item for option in options for item in option['_source']['suggest']]))
        options_with_prefix = [option for option in flat_options if option.startswith(query)]
        options_with_prefix.sort(key=lambda option: len(option))
        return options_with_prefix

    def drilldowns(self, drilldown_names, search_text=None, filters=None):
        return self._search(search_text=search_text, filters=filters, drilldown_names=drilldown_names)

    def search(self, search_text: str, drilldown_names=None, filters=None, ordering=None, page=1, page_size=5):
        # searching in elastic with an empty string returns no hits
        if search_text == "":
            search_text = None
        start_record = page_size * (page - 1) + 1
        result = self.elastic.search(
            index=[index_nl, index_en],
            q=search_text,
            body={'from': start_record,
                  'size': page_size}
        )

        return self.parse_elastic_result(result)

    def get_materials_by_id(self, external_ids, page=1, page_size=5, drilldown_names=None):
        start_record = page_size * (page - 1) + 1
        materials = []
        for external_id in external_ids:
            materials.append(self.elastic.search(
                index=[index_nl, index_en],
                body={
                    "query": {
                        "bool": {
                            "must": [{"match": {"external_id": external_id}}]
                        }
                    },
                    "from": start_record,
                    "size": page_size
                    },
                )
            )
        return materials

    @staticmethod
    def parse_elastic_result(search_result):
        material_keys = ['object_id', 'url', 'title', 'description', 'keywords', 'language', 'aggregationlevel',
                         'publisher', 'publish_datetime', 'author', 'format', 'educationallevels',
                         'themes', 'disciplines']

        result = dict()
        result['recordcount'] = search_result['hits']['total']
        # TODO
        result['drilldowns'] = []

        # TODO
        result['records'] = []
        for result in search_result['hits']['hits']:
            new_material = dict()
            new_material['object_id'] = None  # TODO
            new_material['url'] = result['_source']['url']
            new_material['title'] = result['_source']['title']
            new_material['description'] = result['_source']['text']
            new_material['keywords'] = result['_source']['keywords']
            new_material['language'] = result['_source']['language']
            new_material['aggregationlevel'] = 1  # TODO
            new_material['publisher'] = None  # TODO
            new_material['publish_datetime'] = None  # TODO
            new_material['author'] = None  # TODO
            new_material['format'] = result['_source']['mime_type']
            new_material['disciplines'] = None  # TODO
            new_material['educationallevels'] = None  # TODO
            new_material['themes'] = None  # TODO
            result['records'].append(new_material)
        return result
