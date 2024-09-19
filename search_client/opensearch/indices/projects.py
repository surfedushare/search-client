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
                }
            }
        },
        "mappings": {
            "properties": {
                "external_id": {
                    "type": "keyword"
                },
                "status": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "description": {
                    "type": "text"
                },
                "suggest_completion": {  # auto complete
                    "type": "completion"
                },
                "suggest_phrase": {  # did you mean
                    "type": "text",
                    "analyzer": "trigram"
                },
            }
        }
    }
    return configuration
