from search_client.constants import DocumentTypes


def build_products_index_configuration(product_type: DocumentTypes,
                                       nl_decompound_word_list: str | None = None) -> dict:
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
                        "filter":  ["lowercase", "asciifolding"]
                    },
                    "custom_dutch": {
                        "tokenizer":  "standard",
                        "filter": [
                            "lowercase",
                            "dutch_stop",
                            "dutch_keywords",
                            "dutch_override",
                            "dutch_stemmer",
                        ]
                    },
                },
                "filter": {
                    "dutch_stop": {
                        "type": "stop",
                        "stopwords": "_dutch_"
                    },
                    "shingle": {
                        "type": "shingle",
                        "min_shingle_size": 2,
                        "max_shingle_size": 3
                    },
                    "dutch_keywords": {
                        "type":       "keyword_marker",
                        "keywords":   ["palliatieve"]
                    },
                    "dutch_stemmer": {
                        "type":       "stemmer",
                        "language":   "dutch"
                    },
                    "dutch_override": {
                        "type":       "stemmer_override",
                        "rules": []
                    },
                    "dutch_synonym": {
                        "type": "synonym_graph",
                        "synonyms": [
                            "palliatie, palliatieve"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "authors": {
                    "type": "object",
                    "properties": {
                        "name": {
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
                        "email": {
                            "type": "keyword"
                        },
                        "external_id": {
                            "type": "keyword"
                        },
                        "dai": {
                            "type": "keyword"
                        },
                        "orcid": {
                            "type": "keyword"
                        },
                        "isni": {
                            "type": "keyword"
                        }
                    }
                },
                "publishers": {
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
                "publisher_year": {
                    "type": "keyword"
                },
                "publisher_year_normalized": {
                    "type": "keyword"
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
                "technical_type": {
                    "type": "keyword"
                },
                "technical_types": {
                    "type": "keyword"
                },
                "licenses": {
                    "type": "keyword"
                },
                "harvest_source": {
                    "type": "keyword"
                },
                "is_part_of": {
                    "type": "keyword"
                },
                "has_parts": {
                    "type": "keyword"
                },
                "doi": {
                    "type": "keyword"
                },
                ##########################################
                # Required fields for search client
                ##########################################
                "srn": {  # more like this, get document by srn in the future
                    "type": "keyword"
                },
                "external_id": {  # get document by id
                    "type": "keyword"
                },
                "publisher_date": {  # distance feature and range filtering, deprecated use published_at
                    "type": "date",
                    "format": "strict_date_optional_time||yyyy-MM||epoch_millis"
                },
                "published_at": {  # distance feature and range filtering
                    "type": "date",
                    "format": "strict_date_optional_time||yyyy-MM||epoch_millis"
                },
                "modified_at": {  # distance feature and range filtering
                    "type": "date",
                    "format": "strict_date_optional_time||yyyy-MM||epoch_millis"
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

    # Update the mapping properties with the platform configuration
    match product_type:
        case DocumentTypes.LEARNING_MATERIAL:
            build_search_mapping_properties = build_learning_material_search_mapping_properties
        case DocumentTypes.RESEARCH_PRODUCT:
            build_search_mapping_properties = build_research_product_search_mapping_properties
        case _:
            raise ValueError(f"Unknown document type for building mapper: {product_type}")
    platform_properties = build_search_mapping_properties(nl_decompound_word_list)
    configuration["mappings"]["properties"].update(platform_properties)

    # Update the mapping with language dependent properties
    multilingual_properties = build_multilingual_search_mapping_properties(nl_decompound_word_list)
    configuration["mappings"]["properties"].update(multilingual_properties)

    # Then if our (AWS) environment supports it we add decompound settings
    if nl_decompound_word_list:
        configuration["settings"]["analysis"]["analyzer"]["dutch_dictionary_decompound"] = {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "dutch_stop", "dutch_synonym", "dictionary_decompound"]
        }
        configuration["settings"]["analysis"]["filter"]["dictionary_decompound"] = {
            "type": "dictionary_decompounder",
            "word_list_path": nl_decompound_word_list,
            "updateable": True
        }

    return configuration


def build_multilingual_search_mapping_properties(nl_decompound_word_list: str | None = None):
    nl_search_analyzer = "dutch_dictionary_decompound" if nl_decompound_word_list else "custom_dutch"
    return {
        "language": {"type": "keyword"},
        "texts": {
            "properties": {
                "nl": {
                    "properties": {
                        "titles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "custom_dutch",
                                            "search_analyzer": nl_search_analyzer
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "subtitles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "custom_dutch",
                                            "search_analyzer": nl_search_analyzer
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "descriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "custom_dutch",
                                            "search_analyzer": nl_search_analyzer
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "contents": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "custom_dutch",
                                            "search_analyzer": nl_search_analyzer
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "transcriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "custom_dutch",
                                            "search_analyzer": nl_search_analyzer
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        }
                    }
                },

                "en": {
                    "properties": {
                        "titles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "english",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "subtitles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "english",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "descriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "english",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "contents": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "english",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "transcriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "english",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        }
                    }
                },

                "unk": {
                    "properties": {
                        "titles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "standard",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "subtitles": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "standard",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "descriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "standard",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "contents": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "standard",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                        "transcriptions": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "fields": {
                                        "analyzed": {
                                            "type": "text",
                                            "analyzer": "standard",
                                        },
                                        "folded": {
                                            "type": "text",
                                            "analyzer": "folding"
                                        }
                                    },
                                },
                                "url": {"type": "keyword"},
                                "provider": {"type": "keyword"},
                                "by_machine": {"type": "boolean"},
                            }
                        },
                    },
                },
            }
        }
    }


def build_research_product_search_mapping_properties(nl_decompound_word_list: str | None = None) -> dict:
    return {
        "research_themes": {
            "type": "keyword"
        },
        "research_object_type": {
            "type": "keyword"
        },
        "parties": {
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
        }
    }


def build_learning_material_search_mapping_properties(nl_decompound_word_list: str | None = None) -> dict:
    nl_search_analyzer = "dutch_dictionary_decompound" if nl_decompound_word_list else "custom_dutch"
    return {
        "aggregation_level": {
            "type": "keyword"
        },
        "material_types": {
            "type": "keyword"
        },
        "lom_educational_levels": {
            "type": "keyword"
        },
        "study_vocabulary": {
            "properties": {
                "keyword": {"type": "keyword"},
                "nl": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "custom_dutch",
                            "search_analyzer": nl_search_analyzer
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                "en": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "english",
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                }
            }
        },
        "disciplines": {
            "type": "keyword"
        },
        "disciplines_normalized": {
            "properties": {
                "keyword": {"type": "keyword"},
                "nl": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "custom_dutch",
                            "search_analyzer": nl_search_analyzer
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                "en": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "english",
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                }
            }
        },
        "consortium": {
            "properties": {
                "keyword": {"type": "keyword"},
                "nl": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "custom_dutch",
                            "search_analyzer": nl_search_analyzer
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                },
                "en": {
                    "type": "text",
                    "fields": {
                        "analyzed": {
                            "type": "text",
                            "analyzer": "english",
                        },
                        "folded": {
                            "type": "text",
                            "analyzer": "folding"
                        }
                    }
                }
            }
        },
    }
