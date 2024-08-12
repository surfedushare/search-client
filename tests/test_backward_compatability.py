from unittest import TestCase
import json

from tests.base import BaseOpenSearchTestCase
from search_client.factories.learning_material import generate_nl_material
from search_client.factories.research_product import generate_nl_product
from search_client.serializers.products import LearningMaterial, ResearchProduct


class TestCleaningLegacyExternalIdPrefixes(BaseOpenSearchTestCase):

    def test_legacy_external_id_prefixes(self):
        self.assertEqual(
            self.instance.clean_external_id("edurep_delen:abc"), "WikiwijsDelen:urn:uuid:abc",
            "Expected edurep_delen prefix to get replaced"
        )
        self.assertEqual(self.instance.clean_external_id("abc"), "abc", "Expected Sharekit prefixes to be left alone")
        self.assertEqual(
            self.instance.clean_external_id("surf:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("surfsharekit:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )
        self.assertEqual(
            self.instance.clean_external_id("oer_han:oai:surfsharekit.nl:abc"), "abc",
            "Expected legacy SURF prefix to get replaced"
        )


class TestPydanticToDictConversion(TestCase):

    def test_learning_material_math(self):
        data = generate_nl_material(topic="math")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16T22:35:09+02:00",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Didactiek van wiskundig denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "video": None,
            "harvest_source": "wikiwijsmaken",
            "previews": {
                "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
            },
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
                    "copyright": "cc-by-40",
                    "mime_type": "application/pdf",
                    "access_rights": "OpenAccess",
                    "video": None,
                    "previews": {
                        "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                        "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                        "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-"
                                         "200x150.png"
                    }
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [
                "nerds"
            ],
            "doi": None,
            "lom_educational_levels": [
                "HBO"
            ],
            "disciplines": [
                "exact_informatica"
            ],
            "study_vocabulary": [],
            "technical_type": "document",
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": None,
            "subtitle": None,
            "highlight": {
                "description": [
                    "<em>Materiaal</em> voor lerarenopleidingen"
                ],
                "text": [
                    "Leer<em>materiaal</em> over wiskunde"
                ]
            }
        })

    def test_research_product_math(self):
        data = generate_nl_product(topic="math")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16T22:35:09+02:00",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Onderzoek over wiskundig denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-30",
            "video": None,
            "harvest_source": "wikiwijsmaken",
            "previews": None,
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
                    "copyright": "cc-by-40",
                    "mime_type": "application/pdf",
                    "access_rights": "OpenAccess",
                    "video": None,
                    "previews": {
                        "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                        "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                        "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-"
                                         "200x150.png"
                    }
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [
                "nerds"
            ],
            "doi": "https://doi.org/10.12345",
            "subtitle": None,
            "type": "document",
            "research_object_type": None,
            "parties": [
                "Wikiwijs Maken"
            ],
            "research_themes": [
                "exact_informatica"
            ],
            "projects": [],
            "owners": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "highlight": {
                "description": [
                    "<em>Materiaal</em> voor lerarenopleidingen"
                ],
                "text": [
                    "Leer<em>materiaal</em> over wiskunde"
                ]
            }
        })

    def test_learning_material_biology(self):
        data = generate_nl_material(topic="biology")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16T22:35:09+02:00",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Didactiek van biologisch denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "video": None,
            "harvest_source": "wikiwijsmaken",
            "previews": None,
            "files": [
                {
                    "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35",
                    "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
                    "hash": "16bdc1e9a083ebe1878ec5b867bf850562feff35",
                    "type": "website",
                    "state": "active",
                    "title": "URL 1",
                    "is_link": True,
                    "copyright": "cc-by-40",
                    "mime_type": "text/html",
                    "access_rights": "OpenAccess",
                    "video": None,
                    "previews": None
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "subtitle": None,
            "highlight": {
                "description": None,
                "text": [
                    "Leermateriaal over biologie en didactiek op de <em>universiteit</em>."
                ]
            },
            "lom_educational_levels": [
                "HBO"
            ],
            "disciplines": [
                "aarde_milieu"
            ],
            "study_vocabulary": [],
            "technical_type": "document",
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": None
        })

    def test_research_product_biology(self):
        data = generate_nl_product(topic="biology")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16T22:35:09+02:00",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Onderzoek over biologisch denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-30",
            "video": None,
            "harvest_source": "wikiwijsmaken",
            "previews": None,
            "files": [
                {
                    "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123:16bdc1e9a083ebe1878ec5b867bf850562feff35",
                    "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
                    "hash": "16bdc1e9a083ebe1878ec5b867bf850562feff35",
                    "type": "website",
                    "state": "active",
                    "title": "URL 1",
                    "is_link": True,
                    "copyright": "cc-by-40",
                    "mime_type": "text/html",
                    "access_rights": "OpenAccess",
                    "video": None,
                    "previews": None
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "subtitle": None,
            "highlight": None,
            "type": "document",
            "research_object_type": None,
            "parties": [
                "Wikiwijs Maken"
            ],
            "research_themes": [
                "aarde_milieu"
            ],
            "projects": [],
            "owners": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ]
        })

    def test_learning_material_math_all_languages(self):
        data = generate_nl_material(topic="math_all_languages")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16T22:35:09+02:00",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Didactiek van wiskundig denken (root)",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart (root)",
            "language": "nl",
            "copyright": "cc-by-40",
            "video": None,
            "harvest_source": "wikiwijsmaken",
            "previews": {
                "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-200x150.png"
            },
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
                    "copyright": "cc-by-40",
                    "mime_type": "application/pdf",
                    "access_rights": "OpenAccess",
                    "video": None,
                    "previews": {
                        "full_size": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf.png",
                        "preview": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-400x300.png",
                        "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/pdf-thumbnail-"
                                         "200x150.png"
                    }
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [
                "nerds"
            ],
            "doi": None,
            "lom_educational_levels": [
                "HBO"
            ],
            "disciplines": [
                "exact_informatica"
            ],
            "study_vocabulary": ["http://purl.edustandaard.nl/concept/1ba23d31-f46e-4b40-8c53-fae23b333279"],
            "technical_type": "document",
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": "SURF",
            "subtitle": None,
            "highlight": {
                "description": [
                    "<em>Materiaal</em> voor lerarenopleidingen"
                ],
                "text": [
                    "Leer<em>materiaal</em> over wiskunde"
                ]
            }
        })
