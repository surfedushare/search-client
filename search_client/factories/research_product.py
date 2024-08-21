NL_PRODUCT = {
    "math": {
        "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "set": "sharekit:edusources",
        "title": "Onderzoek over wiskundig denken",
        "text": "Onderzoek over wiskunde en didactiek op de universiteit.",
        "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
        "files": [
            {
                "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10:"
                       "bdd27d20f1182219c6c50714bd4e9d178af38ef6",
                "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
                "hash": "2ad5ffa1ee1b58c84c1adc9acbeff25c",
                "type": "document",
                "state": "active",
                "title": "Didactiek van wiskundig denken.pdf",
                "is_link": True,
                "priority": 0,
                "copyright": "cc-by-40",
                "mime_type": "application/pdf",
                "access_rights": "OpenAccess",
                "previews": {
                    "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                    "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                    "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
                }
            }
        ],
        "description":
        "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op wiskundedidactiek en ICT "
        "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "copyright": "cc-by-30",
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "keywords": ["nerds"],
        "authors": [{"name": "Michel van Ast"}, {"name": "Theo van den Bogaart"}, {"name": "Marc de Graaf"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Onderzoek over wiskunde en didactiek op de universiteit.",
        "suggest_completion": ["Onderzoek", "over", "wiskunde", "en", "didactiek", "op", "de", "universiteit."],
        "doi": "10.12345",
        "technical_type": "document",
        "research_themes": ["exact_informatica"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        },
        "highlight": {
            "description": [
                "<em>Materiaal</em> voor lerarenopleidingen"
            ],
            "text": [
                "Leer<em>materiaal</em> over wiskunde"
            ]
        }
    },
    "biology": {
        "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
        "set": "edurep:wikiwijsmaken",
        "title": "Onderzoek over biologisch denken",
        "text": "Onderzoek over biologie en didactiek op de universiteit.",
        "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
        "files": [
            {
                "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35",
                "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
                "hash": "16bdc1e9a083ebe1878ec5b867bf850562feff35",
                "type": "website",
                "state": "active",
                "title": "URL 1",
                "is_link": True,
                "priority": 0,
                "copyright": "cc-by-40",
                "mime_type": "text/html",
                "access_rights": "OpenAccess"
            }
        ],
        "description":
            "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op biologiedidactiek en ICT "
            "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "wikiwijsmaken:123",
        "copyright": "cc-by-30",
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "keywords": [],
        "authors": [{"name": "Michel van Ast"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Onderzoek over biologie en didactiek op de universiteit.",
        "suggest_completion": ["Onderzoek", "over", "biologie", "en", "didactiek", "op", "de", "universiteit."],
        "doi": None,
        "technical_type": "document",
        "research_themes": ["aarde_milieu"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        }
    },
    "highlight": {
        "text": [
            "Leermateriaal over biologie en didactiek op de <em>universiteit</em>."
        ]
    }
}


def generate_nl_product(title=None, description=None, technical_type=None, source=None, copyright=None,
                        publisher_date=None, studies=None, topic="math", external_id=None):
    copy = NL_PRODUCT[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
    if technical_type:
        copy["technical_type"] = technical_type
    if source:
        copy["harvest_source"] = source
    if source and external_id:
        copy["srn"] = f"{source}:{external_id}"
    if copyright:
        copy["copyright"] = copyright
    if publisher_date:
        copy["publisher_date"] = publisher_date
    if studies:
        copy["studies"] = studies
    return copy


PRODUCT = {
    "math": {
        "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "set": "sharekit:edusources",
        "title": "Onderzoek over wiskundig denken",
        "text": "Onderzoek over wiskunde en didactiek op de universiteit.",
        "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
        "files": [
            {
                "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10:"
                       "bdd27d20f1182219c6c50714bd4e9d178af38ef6",
                "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
                "hash": "2ad5ffa1ee1b58c84c1adc9acbeff25c",
                "type": "document",
                "state": "active",
                "title": "Didactiek van wiskundig denken.pdf",
                "is_link": True,
                "priority": 0,
                "copyright": "cc-by-40",
                "mime_type": "application/pdf",
                "access_rights": "OpenAccess",
                "previews": {
                    "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                    "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                    "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
                }
            }
        ],
        "description":
            "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op wiskundedidactiek en ICT "
            "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "copyright": "cc-by-30",
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "published_at": "2017-04-16T22:35:09+02:00",
        "keywords": ["nerds"],
        "authors": [{"name": "Michel van Ast"}, {"name": "Theo van den Bogaart"}, {"name": "Marc de Graaf"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Onderzoek over wiskunde en didactiek op de universiteit.",
        "suggest_completion": ["Onderzoek", "over", "wiskunde", "en", "didactiek", "op", "de", "universiteit."],
        "doi": "10.12345",
        "technical_type": "document",
        "research_themes": ["exact_informatica"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        },
        "highlight": {
            "description": [
                "<em>Materiaal</em> voor lerarenopleidingen"
            ],
            "text": [
                "Leer<em>materiaal</em> over wiskunde"
            ]
        },
        "texts": {
            "en": {},
            "unk": {},
            "nl": {
                "titles": [
                    {
                        "text": "Onderzoek over wiskundig denken",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
                    }
                ],
                "subtitles": [],
                "descriptions": [
                    {
                        "text": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                                "wiskundedidactiek en ICT met Theo van den Bogaart",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
                    }
                ],
                "contents": [
                    {
                        "text": "Onderzoek over wiskunde en didactiek op de universiteit.",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10:"
                                    "bdd27d20f1182219c6c50714bd4e9d178af38ef6"
                    }
                ],
                "transcriptions": []
            }
        }
    },
    "biology": {
        "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
        "set": "edurep:wikiwijsmaken",
        "title": "Onderzoek over biologisch denken",
        "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
        "files": [
            {
                "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35",
                "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
                "hash": "16bdc1e9a083ebe1878ec5b867bf850562feff35",
                "type": "website",
                "state": "active",
                "title": "URL 1",
                "is_link": True,
                "priority": 0,
                "copyright": "cc-by-40",
                "mime_type": "text/html",
                "access_rights": "OpenAccess"
            }
        ],
        "description":
            "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op biologiedidactiek en ICT "
            "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "wikiwijsmaken:123",
        "copyright": "cc-by-30",
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "published_at": "2017-04-16T22:35:09+02:00",
        "keywords": [],
        "authors": [{"name": "Michel van Ast"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Onderzoek over biologie en didactiek op de universiteit.",
        "suggest_completion": ["Onderzoek", "over", "biologie", "en", "didactiek", "op", "de", "universiteit."],
        "doi": None,
        "technical_type": "document",
        "research_themes": ["aarde_milieu"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        },
        "highlight": {
            "text": [
                "Leermateriaal over biologie en didactiek op de <em>universiteit</em>."
            ]
        },
        "texts": {
            "en": {},
            "unk": {},
            "nl": {
                "titles": [
                    {
                        "text": "Onderzoek over biologisch denken",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123"
                    }
                ],
                "subtitles": [],
                "descriptions": [
                    {
                        "text": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                                "biologiedidactiek en ICT met Theo van den Bogaart",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123"
                    }
                ],
                "contents": [
                    {
                        "text": "Onderzoek over biologie en didactiek op de universiteit.",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35"
                    }
                ],
                "transcriptions": []
            }
        },
    }
}


def generate_product(title=None, description=None, technical_type=None, source=None, copyright=None,
                     publisher_date=None, topic="math", external_id=None):
    copy = PRODUCT[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
    if technical_type:
        copy["technical_type"] = technical_type
    if source:
        copy["harvest_source"] = source
    if source and external_id:
        copy["srn"] = f"{source}:{external_id}"
    if copyright:
        copy["copyright"] = copyright
    if publisher_date:
        copy["publisher_date"] = publisher_date
        copy["published_at"] = publisher_date
    return copy
