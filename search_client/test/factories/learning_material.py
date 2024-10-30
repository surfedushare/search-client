NL_MATERIAL = {
    "math": {
        "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "set": "sharekit:edusources",
        "title": "Didactiek van wiskundig denken",
        "text": "Leermateriaal over wiskunde en didactiek op de universiteit.",
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
        "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op wiskundedidactiek en ICT "
        "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "copyright": "cc-by-40",
        "lom_educational_levels": ["HBO"],
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "keywords": ["nerds"],
        "authors": [{"name": "Michel van Ast"}, {"name": "Theo van den Bogaart"}, {"name": "Marc de Graaf"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Leermateriaal over wiskunde en didactiek op de universiteit.",
        "suggest_completion": ["Leermateriaal", "over", "wiskunde", "en", "didactiek", "op", "de", "universiteit."],
        "study_vocabulary": [],
        "doi": None,
        "technical_type": "document",
        "disciplines": ["exact_informatica"],
        "disciplines_normalized": ["exact_informatica"],
        "learning_material_disciplines_normalized": ["exact_informatica"],
        "previews": {
            "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
            "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
            "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
        },
        "provider": "Wikiwijs Maken"
    },
    "biology": {
        "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
        "set": "edurep:wikiwijsmaken",
        "title": "Didactiek van biologisch denken",
        "text": "Leermateriaal over biologie en didactiek op de universiteit.",
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
            "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op biologiedidactiek en ICT "
            "met Theo van den Bogaart",
        "language": "nl",
        "external_id": "wikiwijsmaken:123",
        "copyright": "cc-by-40",
        "lom_educational_levels": ["HBO"],
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "keywords": [],
        "authors": [{"name": "Michel van Ast"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Leermateriaal over biologie en didactiek op de universiteit.",
        "suggest_completion": ["Leermateriaal", "over", "biologie", "en", "didactiek", "op", "de", "universiteit."],
        "study_vocabulary": [],
        "doi": None,
        "technical_type": "document",
        "disciplines": ["aarde_milieu"],
        "disciplines_normalized": ["aarde_milieu"],
        "learning_material_disciplines_normalized": ["exact_informatica"],
        "provider": "Wikiwijs Maken"
    }
}


def generate_nl_material(educational_levels=None, title=None, description=None, technical_type=None, source=None,
                         copyright=None, publisher_date=None, topic="math", external_id=None):
    copy = NL_MATERIAL[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
    if educational_levels:
        copy["lom_educational_levels"] = educational_levels
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
    return copy


MATERIALS = {
    "math": {
        "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "set": "sharekit:edusources",
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
        "language": "nl",
        "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "copyright": "cc-by-40",
        "licenses": ["cc-by-40"],
        "lom_educational_levels": ["HBO"],
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "published_at": "2017-04-16T22:35:09+02:00",
        "keywords": ["nerds"],
        "authors": [{"name": "Michel van Ast"}, {"name": "Theo van den Bogaart"}, {"name": "Marc de Graaf"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Leermateriaal over wiskunde en didactiek op de universiteit.",
        "suggest_completion": ["Leermateriaal", "over", "wiskunde", "en", "didactiek", "op", "de", "universiteit."],
        "study_vocabulary": {
            "keyword": ["http://purl.edustandaard.nl/concept/1ba23d31-f46e-4b40-8c53-fae23b333279"],
            "nl": ["Robuste statistiek"],
            "en": ["Robust statistics"]
        },
        "doi": None,
        "technical_type": "document",
        "technical_types": ["document"],
        "disciplines": ["exact_informatica"],
        "disciplines_normalized": {
            "keyword": ["exact_informatica"],
            "nl": ["Exact en Informatica"],
            "en": ["Exact sciences and Informatics"]
        },
        "learning_material_disciplines_normalized": ["exact_informatica"],
        "consortium": {
            "keyword": "SURF",
            "nl": "Stichting Universitaire Reken Faciliteiten",
            "en": "Foundation University Computation Facilities"
        },
        "previews": {
            "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
            "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
            "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
        },
        "provider": "Wikiwijs Maken",
        "texts": {
            "en": {},
            "unk": {},
            "nl": {
                "titles": [
                    {
                        "text": "Didactiek van wiskundig denken",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
                    }
                ],
                "subtitles": [],
                "descriptions": [
                    {
                        "text": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                                "wiskundedidactiek en ICT met Theo van den Bogaart",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10"
                    }
                ],
                "contents": [
                    {
                        "text": "Leermateriaal over wiskunde en didactiek op de universiteit.",
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
        "language": "nl",
        "external_id": "wikiwijsmaken:123",
        "copyright": "cc-by-40",
        "licenses": ["cc-by-40"],
        "lom_educational_levels": ["HBO"],
        "publisher_date": "2017-04-16T22:35:09+02:00",
        "published_at": "2017-04-16T22:35:09+02:00",
        "keywords": [],
        "authors": [{"name": "Michel van Ast"}],
        "publishers": ["Wikiwijs Maken"],
        "harvest_source": "wikiwijsmaken",
        "has_parts": [],
        "is_part_of": [],
        "suggest_phrase": "Leermateriaal over biologie en didactiek op de universiteit.",
        "suggest_completion": ["Leermateriaal", "over", "biologie", "en", "didactiek", "op", "de", "universiteit."],
        "study_vocabulary": {
            "keyword": [],
            "en": [],
            "nl": []
        },
        "doi": None,
        "technical_type": "document",
        "technical_types": ["document"],
        "disciplines": ["aarde_milieu"],
        "disciplines_normalized": {
            "keyword": ["aarde_milieu"],
            "nl": ["Aarde en Milieu"],
            "en": ["Earth and Environment"]
        },
        "learning_material_disciplines_normalized": ["aarde_milieu"],
        "consortium": {
            "keyword": None,
            "nl": None,
            "en": None
        },
        "provider": "Wikiwijs Maken",
        "texts": {
            "en": {},
            "unk": {},
            "nl": {
                "titles": [
                    {
                        "text": "Didactiek van biologisch denken",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123"
                    }
                ],
                "subtitles": [],
                "descriptions": [
                    {
                        "text": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                                "biologiedidactiek en ICT met Theo van den Bogaart",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123"
                    }
                ],
                "contents": [
                    {
                        "text": "Leermateriaal over biologie en didactiek op de universiteit.",
                        "provider": "Wikiwijs Maken",
                        "by_machine": False,
                        "document": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35"
                    }
                ],
                "transcriptions": []
            }
        }
    }
}


def generate_material(educational_levels=None, title=None, description=None, technical_type=None, source=None,
                      copyright=None, publisher_date=None, topic="math", external_id=None):
    copy = MATERIALS[topic].copy()
    if title:
        copy["title"] = title
    if description:
        copy["description"] = description
    if external_id:
        copy["external_id"] = external_id
    if educational_levels:
        copy["lom_educational_levels"] = educational_levels
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
        copy["publication_date"] = publisher_date
    return copy
