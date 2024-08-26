from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict

from pydantic import BaseModel
from opensearchpy import OpenSearch, RequestsHttpConnection

from search_client.constants import Platforms, EDUREP_LEGACY_ID_PREFIXES
from search_client.opensearch.configuration import (SearchConfiguration, build_presets_search_configuration,
                                                    MultilingualIndicesSearchConfiguration)


@dataclass(frozen=True, slots=True)
class OpenSearchClientBuilder:
    hosts: list[str]
    use_ssl: bool = False
    http_auth: tuple[str, str] | None = None

    # Some default values that are only relevant when using SSL
    scheme: str = "https"
    port: int = 443
    verify_certs: bool = True

    @classmethod
    def from_host(cls, host: str, http_auth: tuple[str, str] | None = None) -> OpenSearchClientBuilder:
        """
        A convenience method to build a SearchClientBuilder from a single host string.
        """
        use_ssl = host.startswith("https")
        return OpenSearchClientBuilder(hosts=[host], http_auth=http_auth, use_ssl=use_ssl)

    def build(self, check_connection: bool = False) -> OpenSearch:
        connection_configuration = {}
        if self.use_ssl:
            connection_configuration = {
                "use_ssl": True,
                "scheme": self.scheme,
                "port": self.port,
                "verify_certs": self.verify_certs,
            }
        client = OpenSearch(
            hosts=self.hosts,
            http_auth=self.http_auth,
            connection_class=RequestsHttpConnection,
            **connection_configuration
        )
        if check_connection and not client.cat.health(request_timeout=30):
            raise RuntimeError("Unable to connect to Open Search. Perhaps problems with credentials?")
        return client


class SearchClient:

    client: OpenSearch
    configuration: SearchConfiguration

    preset_default: str = "products:multilingual-indices"

    def __init__(self, opensearch_client: OpenSearch, platform: Platforms,
                 configuration: SearchConfiguration | None = None, presets: list[str] | None = None) -> None:
        self.client = opensearch_client
        self.configuration = configuration or build_presets_search_configuration(
            platform, presets, default=self.preset_default
        )

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

        # Transform aggregations
        aggregations_transforms = {}
        for aggregation_name, aggregation in aggregations.items():
            buckets = aggregation["filtered"]["buckets"] if "filtered" in aggregation else aggregation["buckets"]
            for bucket in buckets:
                aggregations_transforms[f"{aggregation_name}-{bucket['key']}"] = bucket["doc_count"]
        aggregation_key = "aggregations" if self.configuration.use_aggregations_over_drilldowns else "drilldowns"
        result[aggregation_key] = aggregations_transforms

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
        result["results"] = [
            self.parse_search_hit(hit)
            for hit in hits['hits']
        ]
        return result

    def parse_search_hit(self, hit: dict) -> BaseModel:
        """
        Parses the search hit into the format that is also used by the edurep endpoint.
        It's mostly just mapping the variables we need into the places that we expect them to be.
        :param hit: result from search
        :return BaseModel: parsed data through Pydantic
        """
        if "_index" not in hit:
            raise ValueError("Search hit did not specify an index.")
        data = hit["_source"]
        data["score"] = hit.get("_score", 1.00)
        data["highlight"] = self.parse_hit_highlight(hit.get("highlight"))
        serializer_model = self.configuration.get_serializer_from_index(hit["_index"])
        return serializer_model(**data)

    def parse_hit_highlight(self, highlight: dict) -> dict | None:
        if not highlight:
            return
        result = defaultdict(list)
        for field, snippets in highlight.items():
            field_reference = self.configuration.extrapolate_field_references(field)[0]
            highlight_key = next(
                (key for key, references in self.configuration.highlights.items() if field_reference in references)
            )
            result[highlight_key] += snippets
        return result

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
            index=self.configuration.get_aliases(),
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
        This method is deprecated in favour of aggregations, which functions the same,
        but takes "drilldown_names" from SearchConfiguration.filter_fields automatically.
        """
        search_results = self.search(search_text=search_text, filters=filters, drilldown_names=drilldown_names)
        search_results["results"] = []
        search_results.update(self.parse_results_total(0))
        return search_results

    def aggregations(self, search_text: str = None, filters: list[dict] = None) -> dict:
        """
        This method executes a search with its parameters, but strips the results.
        This leaves a response with only filter counts data.

        :param search_text: A string to search for.
        :param filters: The filters that are applied for this search.
        :return:
        """
        search_results = self.search(search_text=search_text, filters=filters, aggregate_filter_counts=True)
        search_results["results"] = []
        search_results.update(self.parse_results_total(0))
        return search_results

    def search(self, search_text: str, drilldown_names: list[str] = None, filters: list[dict] = None,
               ordering: str = None, page: int = 1, page_size: int = 5, min_score: float = 0.00,
               aggregate_filter_counts: bool = False) -> dict:
        """
        Build and send a query to search engine and parse it before returning.

        :param search_text: A string to search for.
        :param drilldown_names: A list of the 'drilldowns' (filters) that are to be counted by engine (deprecated)
        :param filters: The filters that are applied for this search.
        :param ordering: Sort the results by this ordering (or use default search ordering otherwise)
        :param page: The page index of the results
        :param page_size: How many items are loaded per page.
        :param min_score: The minimal score for a result to be included in the response
        :param aggregate_filter_counts: Indicates whether counts for filters should be calculated
        :return:
        """
        aggregate_filter_counts = aggregate_filter_counts or bool(drilldown_names)

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
                   field: {} for field in self.configuration.get_highlight_fields()
                }
            }
        }

        if search_text:
            query_string = {
                "simple_query_string": {
                    "fields": self.configuration.search_fields,
                    "query": search_text,
                    "default_operator": "and"
                }
            }
            body["query"]["bool"]["must"] += [query_string]
            if self.configuration.distance_feature_field:
                body["query"]["bool"]["should"] = {
                    "distance_feature": {
                        "field": self.configuration.distance_feature_field,
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

        if aggregate_filter_counts:
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

    @staticmethod
    def clean_external_id(external_id: str) -> str:
        for legacy_prefix, prefix in EDUREP_LEGACY_ID_PREFIXES.items():
            if external_id.startswith(legacy_prefix):
                external_id = external_id.replace(legacy_prefix, prefix, 1)
                break
        return external_id

    def get_documents_by_srn(self, document_ids: list[str], page: int = 1, page_size: int = 10) -> dict:
        return self.get_documents_by_id(document_ids=document_ids, page=page, page_size=page_size, id_field="_id")

    def get_documents_by_id(self, document_ids: list[str] = None, page: int = 1, page_size: int = 10,
                            external_ids: list[str] = None, id_field: str = "external_id") -> dict:
        """
        Retrieve specific materials from search engine through their external id.

        :param document_ids: the id's of the materials to retrieve
        :param external_ids: same as document_ids, but deprecated use document_ids instead
        :param page: The page index of the results
        :param page_size: How many items are loaded per page.
        :param id_field: Which field to use for the lookup of the documents by id (default: external_id)
        :return: a list of search results (like a regular search).
        """
        document_ids = document_ids if document_ids else external_ids
        start_record = page_size * (page - 1)

        corrected_ids = []
        if id_field == "external_id":
            for external_id in document_ids:
                corrected_ids.append(self.clean_external_id(external_id))
        else:
            corrected_ids = document_ids

        raw_result = self.client.search(
            index=self.configuration.get_aliases(),
            body={
                "query": {
                    "bool": {
                        "must": [{"terms": {id_field: corrected_ids}}]
                    }
                },
                'from': start_record,
                'size': page_size,
            },
        )
        search_result = self.parse_search_result(raw_result)
        id_attribute = id_field if id_field != "_id" else "srn"
        documents = {
            getattr(document, id_attribute): document
            for document in search_result["results"]
        }
        results = []
        for document_id in corrected_ids:
            if document_id not in documents:
                continue
            results.append(documents[document_id])
        search_result.update(self.parse_results_total(len(results)))
        search_result["results"] = results
        return search_result

    def stats(self) -> dict | int:
        if not self.configuration.allow_multi_entity_results:
            stats = self.client.count(index=",".join(self.configuration.get_aliases()))
            return stats.get("count", 0)
        stats = {}
        total = 0
        for entity, alias in self.configuration.get_aliases_by_entity().items():
            response = self.client.count(index=alias)
            count = response.get("count", 0)
            total += count
            stats[entity.value] = count
        stats["documents"] = total
        return stats

    def more_like_this(self, identifier: str, language: str, transform_results: bool = False,
                       is_external_identifier: bool = True) -> dict:
        # As long as frontends are not using SRN we need to allow comparisons on external_id
        if is_external_identifier:
            results = self.get_documents_by_id([identifier])
            # If we can't find the referenced document we return no results
            if not results["results"]:
                result = self.parse_results_total(0)
                result["results"] = []
                return result
            doc = results["results"][0]
            identifier = doc.srn

        # Now that we have a SRN value as identifier we can continue as normal
        indices = self.configuration.get_aliases_by_language()
        index = indices.get(language, indices["unk"])
        field_names = self.configuration.interpolate_field_languages(
            *self.configuration.more_like_this_field_references
        )
        body = {
            "query": {
                "more_like_this": {
                    "fields": field_names,
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
        result = self.parse_results_total(hits["total"])
        result["results"] = [
            self.parse_search_hit(hit)
            for hit in hits["hits"]
        ]
        return result

    def author_suggestions(self, author_name: str) -> dict:
        body = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "fields": [field for field in self.configuration.search_fields if "authors" not in field],
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
            index=self.configuration.get_aliases(),
            body=body
        )
        hits = search_result.pop("hits")
        result = self.parse_results_total(hits["total"])
        result["results"] = [
            self.parse_search_hit(hit)
            for hit in hits["hits"]
        ]
        return result

    def parse_filters(self, filters: list[dict]) -> list[dict]:
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
            if not filter_item['items']:
                continue
            # if documents are separated by language in indices, we can't use "language" as a traditional filter
            support_multilingual_indices = isinstance(self.configuration, MultilingualIndicesSearchConfiguration)
            if 'language' in filter_item['external_id'] and support_multilingual_indices:
                continue
            search_type = filter_item['external_id']
            # date range query
            if search_type in self.configuration.range_filter_fields:
                lower_bound, upper_bound = filter_item["items"]
                if lower_bound is not None or upper_bound is not None:
                    filter_items.append({
                        "range": {
                            search_type: {
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
        aggregation_names = aggregation_names or list(self.configuration.filter_fields)
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

    @staticmethod
    def parse_results_total(total: dict | int) -> dict:
        if isinstance(total, int):  # the total did not come from OpenSearch directly, but was deferred somehow
            total = {"value": total, "relation": "eq"}
        return {
            "results_total": {
                "value": total["value"],
                "is_precise": total["relation"] != "gte"
            }
        }

    def parse_index_language(self, filters: list[dict]) -> list[str]:
        """
        Select the index to search on based on language.
        """
        # if no language is selected, search on both.
        indices = self.configuration.get_aliases()
        if not filters or not isinstance(self.configuration, MultilingualIndicesSearchConfiguration):
            return indices
        language_item = [filter_item for filter_item in filters if filter_item['external_id'] == 'language.keyword']
        if not language_item:
            return indices
        language_indices = [f"{self.configuration.platform.value}-{language}" for language in language_item[0]['items']]
        return language_indices if len(language_indices) else indices
