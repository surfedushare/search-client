def build_projects_index_configuration() -> dict:
    configuration = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "analysis": {
                "analyzer": {
                    "trigram": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "shingle"]
                    },
                    "folding": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "asciifolding"]
                    },
                }
            }
        },
        "mappings": {
            "properties": {
                "project_status": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "goal": {
                    "type": "text"
                },
                "approach": {
                    "type": "text"
                },
                "results": {
                    "type": "text"
                },
                "keywords": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                "parties": {
                    "type": "keyword"
                },
                "products": {
                    "type": "keyword"
                },
                "themes": {
                    "type": "keyword"
                },
                "sia_project_reference": {
                    "type": "keyword"
                },
                ##########################################
                # Required fields for search client
                ##########################################
                "srn": {  # get document by srn
                    "type": "keyword"
                },
                "external_id": {  # get document by id
                    "type": "keyword"
                },
                "suggest_completion": {  # auto complete
                    "type": "completion"
                },
                "suggest_phrase": {  # did you mean
                    "type": "text",
                    "analyzer": "trigram"
                },
                "provider": {  # a cross-entity filter field
                    "type": "keyword",
                    "fields": {
                        "filter_search": {  # dirty fix to allow "filtering" by provider for Publinova through search
                            "type": "text",
                        }
                    }
                },
            }
        }
    }
    return configuration
