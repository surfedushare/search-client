NL_MATERIAL = {
    "math": {
        "srn": "wikiwijsmaken:3522b79c-928c-4249-a7f7-d2bcb3077f10",
        "title": "Onderzoek over wiskundig denken",
        "text": "Onderzoek over wiskunde en didactiek op de universiteit.",
        "url": "https://maken.wikiwijs.nl/91192/Wiskundedidactiek_en_ICT",
        "files": [
            {
                "mime_type": "application/x-zip",
                "url": "https://maken.wikiwijs.nl/91192/Wiskundedidactiek_en_ICT",
                "title": "Wiskundedidactiek_en_ICT"
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
        "analysis_allowed": True,
        "ideas": [],
        "doi": None,
        "technical_type": "document",
        "research_themes": ["exact_informatica"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        }
    },
    "biology": {
        "srn": "wikiwijsmaken:wikiwijsmaken:123",
        "title": "Onderzoek over biologisch denken",
        "text": "Onderzoek over biologie en didactiek op de universiteit.",
        "url": "https://maken.wikiwijs.nl/91192/Biologiedidactiek_en_ICT",
        "files": [
            {
                "mime_type": "application/x-zip",
                "url": "https://maken.wikiwijs.nl/91192/Biologiedidactiek_en_ICT",
                "title": "Biologiedidactiek_en_ICT"
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
        "analysis_allowed": True,
        "ideas": [],
        "doi": None,
        "technical_type": "document",
        "research_themes": ["aarde_milieu"],
        "provider": {
            "ror": None,
            "external_id": None,
            "name": "Wikiwijs Maken",
            "slug": None
        }
    }
}


def generate_nl_product(title=None, description=None, technical_type=None, source=None, copyright=None,
                        publisher_date=None, studies=None, topic="math", external_id=None):
    copy = NL_MATERIAL[topic].copy()
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
