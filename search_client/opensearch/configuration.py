from search_client.constants import DocumentTypes


def create_open_search_index_configuration(lang: str, document_type: DocumentTypes,
                                           decompound_word_list: str | None = None) -> dict:
    language_analyzers = {
        'nl': 'custom_dutch',
        'en': 'english'
    }
    search_analyzer = language_analyzers.get(lang, "standard")
    if decompound_word_list and lang == "nl":
        search_analyzer = "dutch_dictionary_decompound"
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
        'mappings': {
            'properties': {
                'title': {
                    'type': 'text',
                    'fields': {
                        'analyzed': {
                            'type': 'text',
                            'analyzer': language_analyzers.get(lang, "standard"),
                            'search_analyzer': search_analyzer,
                        },
                        'folded': {
                            'type': 'text',
                            'analyzer': 'folding'
                        }
                    }
                },
                'text': {
                    'type': 'text',
                    'fields': {
                        'analyzed': {
                            'type': 'text',
                            'analyzer': language_analyzers.get(lang, "standard"),
                            'search_analyzer': search_analyzer,
                        },
                        'folded': {
                            'type': 'text',
                            'analyzer': 'folding'
                        }
                    }
                },
                'description': {
                    'type': 'text',
                    'fields': {
                        'analyzed': {
                            'type': 'text',
                            'analyzer': language_analyzers.get(lang, "standard"),
                            'search_analyzer': search_analyzer,
                        },
                        'folded': {
                            'type': 'text',
                            'analyzer': 'folding'
                        }
                    }
                },
                'url': {'type': 'text'},
                'authors': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'text',
                            'fields': {
                                'keyword': {
                                    'type': 'keyword',
                                    'ignore_above': 256
                                },
                                'folded': {
                                    'type': 'text',
                                    'analyzer': 'folding'
                                }
                            }
                        },
                        'email': {
                            'type': 'keyword'
                        },
                        'external_id': {
                            'type': 'keyword'
                        },
                        'dai': {
                            'type': 'keyword'
                        },
                        'orcid': {
                            'type': 'keyword'
                        },
                        'isni': {
                            'type': 'keyword'
                        }
                    }
                },
                'publishers': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword',
                            'ignore_above': 256
                        },
                        'folded': {
                            'type': 'text',
                            'analyzer': 'folding'
                        }
                    }
                },
                'publisher_date': {
                    'type': 'date',
                    'format': 'strict_date_optional_time||yyyy-MM||epoch_millis'
                },
                'publisher_year': {
                    'type': 'keyword'
                },
                'publisher_year_normalized': {
                    'type': 'keyword'
                },
                'modified_at': {
                    'type': 'date',
                    'format': 'strict_date_optional_time||yyyy-MM||epoch_millis'
                },
                'keywords': {
                    'type': 'text',
                    'fields': {
                        'keyword': {
                            'type': 'keyword',
                            'ignore_above': 256
                        },
                        'folded': {
                            'type': 'text',
                            'analyzer': 'folding'
                        }
                    }
                },
                'technical_type': {
                    'type': 'keyword'
                },
                'id': {'type': 'text'},
                'external_id': {
                    'type': 'keyword'
                },
                'harvest_source': {
                    'type': 'keyword'
                },
                "suggest_completion": {
                    "type": "completion"
                },
                "suggest_phrase": {
                    "type": "text",
                    "analyzer": "trigram"
                },
                'is_part_of': {
                    'type': 'keyword'
                },
                'has_parts': {
                    'type': 'keyword'
                }
            }
        }
    }

    # Update the mapping properties with the project configuration
    match document_type:
        case DocumentTypes.LEARNING_MATERIAL:
            get_search_mapping_properties = get_learning_material_search_mapping_properties
        case DocumentTypes.RESEARCH_PRODUCT:
            get_search_mapping_properties = get_research_product_search_mapping_properties
        case _:
            raise ValueError(f"Unknown document type for building mapper: {document_type}")
    configuration["mappings"]["properties"].update(get_search_mapping_properties())

    # Then if our (AWS) environment supports it we add decompound settings
    if decompound_word_list:
        configuration["settings"]["analysis"]["analyzer"]["dutch_dictionary_decompound"] = {
            "type": "custom",
            "tokenizer": "standard",
            "filter": ["lowercase", "dutch_stop", "dutch_synonym", "dictionary_decompound"]
        }
        configuration["settings"]["analysis"]["filter"]["dictionary_decompound"] = {
            "type": "dictionary_decompounder",
            "word_list_path": decompound_word_list,
            "updateable": True
        }

    return configuration


def get_research_product_search_mapping_properties():
    return {
        'research_themes': {
            'type': 'keyword'
        },
        'research_object_type': {
            'type': 'keyword'
        },
        'parties': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': 256
                },
                'folded': {
                    'type': 'text',
                    'analyzer': 'folding'
                }
            }
        },
        'projects': {
            'type': 'text',
            'fields': {
                'keyword': {
                    'type': 'keyword',
                    'ignore_above': 256
                },
                'folded': {
                    'type': 'text',
                    'analyzer': 'folding'
                }
            }
        },
        'extension': {
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'text',
                },
                'is_addition': {
                    'type': 'boolean'
                }
            }
        },
    }


def get_learning_material_search_mapping_properties():
    return {
        'aggregation_level': {
            'type': 'keyword'
        },
        'doi': {
            'type': 'keyword'
        },
        'material_types': {
            'type': 'keyword'
        },
        'lom_educational_levels': {
            'type': 'keyword'
        },
        'disciplines': {
            'type': 'keyword'
        },
        'study_vocabulary': {
            'type': 'keyword'
        },
        'learning_material_disciplines': {
            'type': 'keyword'
        },
        'learning_material_disciplines_normalized': {
            'type': 'keyword'
        },
        'consortium': {
            'type': 'keyword'
        },
    }
