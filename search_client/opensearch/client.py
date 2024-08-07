from collections import defaultdict

from rest_framework.serializers import Serializer
from opensearchpy import OpenSearch, RequestsHttpConnection

from search_client.constants import DocumentTypes, SEARCH_FIELDS, EDUREP_LEGACY_ID_PREFIXES
from search_client.serializers import SimpleLearningMaterialResultSerializer, ResearchProductResultSerializer


class SearchClient:

    def __init__(self, host: str, document_type: DocumentTypes, alias_prefix: str,
                 verify_certs: bool = True, basic_auth: tuple[str, str] = None,
                 search_results_key: str = "results") -> None:
        protocol_config = {}
        if host.startswith("https"):
            protocol_config = {
                "scheme": "https",
                "port": 443,
                "use_ssl": True,
                "verify_certs": verify_certs,
            }

        self.client = OpenSearch(
            [host],
            http_auth=basic_auth,
            connection_class=RequestsHttpConnection,
            **protocol_config
        )
        self.document_type = document_type
        self.alias_prefix = alias_prefix
        self.index_nl = f"{alias_prefix}-nl"
        self.index_en = f"{alias_prefix}-en"
        self.index_unk = f"{alias_prefix}-unk"
        self.search_results_key = search_results_key
        self.languages = {
            "nl": self.index_nl,
            "en": self.index_en
        }

    def __str__(self) -> str:
        return f"<SearchClient({self.client})>"

    def parse_search_result(self, search_result: dict) -> dict:
        """
        Parses the search result into the correct format that the frontend uses

        :param search_result: result from search
        :return result: list of results ready for frontend
        """
        hits = search_result.pop("hits")
        aggregations = search_result.get("aggregations", {})
        result = self.parse_results_total(hits['total'])

        # Transform aggregations into drilldowns
        drilldowns = {}
        for aggregation_name, aggregation in aggregations.items():
            buckets = aggregation["filtered"]["buckets"] if "filtered" in aggregation else aggregation["buckets"]
            for bucket in buckets:
                drilldowns[f"{aggregation_name}-{bucket['key']}"] = bucket["doc_count"]
        result['drilldowns'] = drilldowns

        # Parse spelling suggestions
        did_you_mean = {}
        if 'suggest' in search_result:
            spelling_suggestion = search_result['suggest']['did-you-mean-suggestion'][0]
            spelling_option = spelling_suggestion['options'][0] if len(spelling_suggestion['options']) else None
            if spelling_option is not None and spelling_option["score"] >= 0.01:
                did_you_mean = {
                    'original': spelling_suggestion['text'],
                    'suggestion': spelling_option['text']
                }
        result['did_you_mean'] = did_you_mean

        # Transform hits into records
        result[self.search_results_key] = [
            self.parse_search_hit(hit)
            for hit in hits['hits']
        ]
        return result

    def get_result_serializer(self) -> Serializer | None:
        match self.document_type:
            case DocumentTypes.LEARNING_MATERIAL:
                return SimpleLearningMaterialResultSerializer()
            case DocumentTypes.RESEARCH_PRODUCT:
                return ResearchProductResultSerializer()
            case _:
                raise TypeError(f"Unknown document type for result serialization: {self.document_type}")

    def parse_search_hit(self, hit: dict, transform: bool = True) -> dict:
        """
        Parses the search hit into the format that is also used by the edurep endpoint.
        It's mostly just mapping the variables we need into the places that we expect them to be.
        :param hit: result from search
        :param transform: will apply a transformation based on serializer fields when set to True
        :return record: parsed record
        """
        data = hit["_source"]
        data["score"] = hit.get("_score", 1.00)
        serializer = self.get_result_serializer()
        # Basic mapping between field and data (excluding any method fields with a source of "*")
        field_mapping = {
            field.source: field_name if transform else field.source
            for field_name, field in serializer.fields.items() if field.source != "*"
        }
        record = {
            field_mapping[field]: value
            for field, value in data.items() if field in field_mapping
        }
        # Calling methods on serializers to set data for method fields
        for field_name, field in serializer.fields.items():
            if field.source != "*":
                continue
            record[field_name] = getattr(serializer, field.method_name)(data)

        # Add highlight to the record
        if hit.get("highlight", 0):
            record["highlight"] = hit["highlight"]

        return record

    def autocomplete(self, query: str) -> list[str]:
        """
        Use the suggest query to get typing hints during searching.

        :param query: the input from the user so far
        :return: a list of options matching the input query, sorted by length
        """
        # build the query for search engine
        query_dictionary = {
            'suggest': {
                "autocomplete": {
                    'text': query,
                    "completion": {
                        "field": "suggest_completion",
                        "size": 100
                    }
                }
            }
        }

        result = self.client.search(
            index=[self.index_nl, self.index_en, self.index_unk],
            body=query_dictionary
        )

        # extract the options from the search result, remove duplicates,
        # remove non-matching prefixes (engine will suggest things that don't match _exactly_)
        # and sort by length
        autocomplete = result['suggest']['autocomplete']
        options = autocomplete[0]['options']
        flat_options = list(set([item for option in options for item in option['_source']['suggest_completion']]))
        options_with_prefix = [option for option in flat_options if option.lower().startswith(query.lower())]
        options_with_prefix.sort(key=lambda option: len(option))
        return options_with_prefix

    def drilldowns(self, drilldown_names: list[str], search_text: str = None, filters: list[dict] = None) -> dict:
        """
        This function is named drilldowns is because it's also named drilldowns in the original edurep search code.
        It passes on information to search, and returns the search without the records.
        This allows calculation of 'item counts' (i.e. how many results there are in through a certain filter)
        """
        search_results = self.search(search_text=search_text, filters=filters, drilldown_names=drilldown_names)
        search_results[self.search_results_key] = []
        search_results.update(self.parse_results_total(0))
        return search_results

    def search(self, search_text: str, drilldown_names: list[str] = None, filters: list[dict] = None,
               ordering: str = None, page: int = 1, page_size: int = 5, min_score: float = 0.00) -> dict:
        """
        Build and send a query to search engine and parse it before returning.

        :param search_text: A string to search for.
        :param drilldown_names: A list of the 'drilldowns' (filters) that are to be counted by engine.
        :param filters: The filters that are applied for this search.
        :param ordering: Sort the results by this ordering (or use default search ordering otherwise)
        :param page: The page index of the results
        :param page_size: How many items are loaded per page.
        :return:
        """

        start_record = page_size * (page - 1)
        body = {
            'query': {
                "bool": defaultdict(list)
            },
            'min_score': min_score,
            'from': start_record,
            'size': page_size,
            'post_filter': {
                "bool": defaultdict(list)
            },
            'highlight': {
                'number_of_fragments': 1,
                'fragment_size': 120,
                'fields': {
                    'description': {},
                    'text': {}
                }
            }
        }

        if search_text:
            query_string = {
                "simple_query_string": {
                    "fields": SEARCH_FIELDS[self.document_type],
                    "query": search_text,
                    "default_operator": "and"
                }
            }
            body["query"]["bool"]["must"] += [query_string]
            body["query"]["bool"]["should"] = {
                "distance_feature": {
                    "field": "publisher_date",
                    "pivot": "90d",
                    "origin": "now",
                    "boost": 1.15
                }
            }
            body["suggest"] = {
                'did-you-mean-suggestion': {
                    'text': search_text,
                    'phrase': {
                        'field': 'suggest_phrase',
                        'size': 1,
                        'gram_size': 3,
                        'direct_generator': [{
                            'field': 'suggest_phrase',
                            'suggest_mode': 'always'
                        }],
                    },
                }
            }

        indices = self.parse_index_language(filters)

        if drilldown_names:
            body["aggs"] = self.parse_aggregations(drilldown_names, filters)

        filters = self.parse_filters(filters)
        if filters:
            body["post_filter"]["bool"]["must"] += filters

        if ordering:
            body["sort"] = [
                self.parse_ordering(ordering),
                "_score"
            ]
        # make query and parse
        result = self.client.search(
            index=indices,
            body=body
        )
        return self.parse_search_result(result)

    def get_materials_by_id(self, external_ids: list[str], page: int = 1, page_size: int = 10, **kwargs) -> dict:
        return self.get_documents_by_id(external_ids, page, page_size)

    def clean_external_id(self, external_id: str) -> str:
        for legacy_prefix, prefix in EDUREP_LEGACY_ID_PREFIXES.items():
            if external_id.startswith(legacy_prefix):
                external_id = external_id.replace(legacy_prefix, prefix, 1)
                break
        return external_id

    def get_documents_by_id(self, external_ids: list[str], page: int = 1, page_size: int = 10) -> dict:
        """
        Retrieve specific materials from search engine through their external id.

        :param external_ids: the id's of the materials to retrieve
        :param page: The page index of the results
        :param page_size: How many items are loaded per page.
        :return: a list of search results (like a regular search).
        """
        start_record = page_size * (page - 1)

        corrected_external_ids = []
        for external_id in external_ids:
            corrected_external_ids.append(self.clean_external_id(external_id))

        raw_result = self.client.search(
            index=[self.index_nl, self.index_en, self.index_unk],
            body={
                "query": {
                    "bool": {
                        "must": [{"terms": {"external_id": corrected_external_ids}}]
                    }
                },
                'from': start_record,
                'size': page_size,
            },
        )
        search_result = self.parse_search_result(raw_result)
        documents = {
            document["external_id"]: document
            for document in search_result[self.search_results_key]
        }
        results = []
        for external_id in corrected_external_ids:
            if external_id not in documents:
                continue
            results.append(documents[external_id])
        search_result.update(self.parse_results_total(len(results)))
        search_result[self.search_results_key] = results
        return search_result

    def stats(self) -> dict:
        stats = self.client.count(index=",".join([self.index_nl, self.index_en, self.index_unk]))
        return stats.get("count", 0)

    def more_like_this(self, identifier: str, language: str, transform_results: bool = False,
                       is_external_identifier: bool = True) -> dict:
        # As long as frontends are not using SRN we need to allow comparisons on external_id
        if is_external_identifier:
            results = self.get_documents_by_id([identifier])
            # If we can't find the referenced document we return no results
            if not results[self.search_results_key]:
                result = self.parse_results_total(0, is_search=False)
                result["results"] = []
                return result
            doc = results[self.search_results_key][0]
            identifier = doc.get("srn", identifier)

        # Now that we have a SRN value as identifier we can continue as normal
        index = self.languages.get(language, self.index_unk)
        body = {
            "query": {
                "more_like_this": {
                    "fields": ["title", "description"],
                    "like": [
                        {
                            "_index": index,
                            "_id": identifier
                        }
                    ],
                    "min_term_freq": 1,
                    "max_query_terms": 12
                }
            }
        }
        search_result = self.client.search(
            index=index,
            body=body
        )
        hits = search_result.pop("hits")
        result = self.parse_results_total(hits["total"], is_search=False)
        result["results"] = [
            self.parse_search_hit(hit, transform=transform_results)
            for hit in hits["hits"]
        ]
        return result

    def author_suggestions(self, author_name: str, transform_results: bool = False) -> dict:
        body = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "fields": [field for field in SEARCH_FIELDS[self.document_type] if "authors" not in field],
                            "query": author_name,
                        },
                    },
                    "must_not": {
                        "match": {"authors.name.keyword": author_name}
                    }
                }
            }
        }
        search_result = self.client.search(
            index=[self.index_nl, self.index_en, self.index_unk],
            body=body
        )
        hits = search_result.pop("hits")
        result = self.parse_results_total(hits["total"], is_search=False)
        result["results"] = [
            self.parse_search_hit(hit, transform=transform_results)
            for hit in hits["hits"]
        ]
        return result

    @staticmethod
    def parse_filters(filters: list[dict]) -> list[dict]:
        """
        Parse filters from the frontend format into the search engine format.
        Not every filter is handled by search engine  in the same way so it's a lot of manual parsing.

        :param filters: the list of filters to be parsed
        :return: the filters in the format for a search query.
        """
        if not filters:
            return []
        filter_items = []
        for filter_item in filters:
            # skip filter_items that are empty
            # and the language filter item (it's handled by telling search engine in what index to search).
            if not filter_item['items'] or 'language.keyword' in filter_item['external_id']:
                continue
            search_type = filter_item['external_id']
            # date range query
            if search_type == "publisher_date":
                lower_bound, upper_bound = filter_item["items"]
                if lower_bound is not None or upper_bound is not None:
                    filter_items.append({
                        "range": {
                            "publisher_date": {
                                "gte": lower_bound,
                                "lte": upper_bound
                            }
                        }
                    })
            # all other filter types are handled by just using terms with the 'translated' filter items
            else:
                filter_items.append({
                    "terms": {
                        search_type: filter_item["items"]
                    }
                })
        return filter_items

    def parse_aggregations(self, aggregation_names: list[str], filters: list[dict]) -> dict:
        """
        Parse the aggregations so search engine can count the items properly.

        :param aggregation_names: the names of the aggregations to
        :param filters: the filters for the query
        :return:
        """

        aggregation_items = {}
        for aggregation_name in aggregation_names:
            other_filters = []

            if filters:
                other_filters = list(filter(lambda x: x['external_id'] != aggregation_name, filters))
                other_filters = self.parse_filters(other_filters)

            search_type = aggregation_name

            if len(other_filters) > 0:
                # Filter the aggregation by the filters applied to other categories
                aggregation_items[aggregation_name] = {
                    "filter": {
                        "bool": {
                            "must": other_filters
                        }
                    },
                    "aggs": {
                        "filtered": {
                            "terms": {
                                "field": search_type,
                                "size": 2000,
                            }
                        }
                    },
                }
            else:
                aggregation_items[aggregation_name] = {
                    "terms": {
                        "field": search_type,
                        "size": 2000,
                    }
                }
        return aggregation_items

    @staticmethod
    def parse_ordering(ordering: str) -> dict:
        """
        Parse the frontend ordering format ('asc', 'desc' or None) into the type that search engine expects.
        """
        order = "asc"
        if ordering.startswith("-"):
            order = "desc"
            ordering = ordering[1:]
        return {ordering: {"order": order}}

    def parse_results_total(self, total: dict | int, is_search: bool = True) -> dict:
        if isinstance(total, int):  # the total did not come from OpenSearch directly, but was deferred somehow
            total = {"value": total, "relation": "eq"}
        total_key = f"{self.search_results_key}_total" if is_search else "results_total"
        legacy_total_key = "recordcount" if is_search else "records_total"
        return {
            total_key: {
                "value": total["value"],
                "is_precise": total["relation"] != "gte"
            },
            legacy_total_key: total["value"]
        }

    def parse_index_language(self, filters: list[dict]) -> list[str]:
        """
        Select the index to search on based on language.
        """
        # if no language is selected, search on both.
        indices = [self.index_nl, self.index_en, self.index_unk]
        if not filters:
            return indices
        language_item = [filter_item for filter_item in filters if filter_item['external_id'] == 'language.keyword']
        if not language_item:
            return indices
        language_indices = [f"{self.alias_prefix}-{language}" for language in language_item[0]['items']]
        return language_indices if len(language_indices) else indices
