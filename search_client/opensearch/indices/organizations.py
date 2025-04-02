def build_organizations_index_configuration() -> dict:
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
                "name": {
                    "type": "text",
                    "fields": {
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                "description": {
                    "type": "text",
                    "fields": {
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                ##########################################
                # Required fields for search client
                ##########################################
                "srn": {  # get document by srn
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
                    "type": "keyword"
                },
            }
        }
    }
    return configuration
