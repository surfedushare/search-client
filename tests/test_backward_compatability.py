from unittest import TestCase
import json

from tests.base import SearchClientTestCase
from search_client.test.factories import generate_nl_material, generate_material, generate_nl_product, generate_product
from search_client.serializers.products import LearningMaterial, ResearchProduct


class TestCleaningLegacyExternalIdPrefixes(SearchClientTestCase):

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
            "entity": "products",
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Didactiek van wiskundig denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": [],
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
                    "priority": 0,
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
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
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
            "technical_types": [],
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "metrics": {
                "views": 1,
                "stars": {
                    "average": 5.0,
                    "star_1": 0,
                    "star_2": 0,
                    "star_3": 0,
                    "star_4": 0,
                    "star_5": 1
                }
            },
        })

    def test_research_product_math(self):
        data = generate_nl_product(topic="math")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "entity": "products",
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Onderzoek over wiskundig denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": [],
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
                    "priority": 0,
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
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [
                "nerds"
            ],
            "doi": "https://doi.org/10.12345",
            "sia_project_id": None,
            "subtitle": None,
            "type": "document",
            "types": [],
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
                    "external_id": None,
                    "is_external": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                }
            ],
            "highlight": None,  # only gets added during actual search
            "metrics": {
                "views": 1,
                "stars": {
                    "average": 5.0,
                    "star_1": 0,
                    "star_2": 0,
                    "star_3": 0,
                    "star_4": 0,
                    "star_5": 1
                }
            },
        })

    def test_learning_material_biology(self):
        data = generate_nl_material(topic="biology")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "entity": "products",
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Didactiek van biologisch denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": [],
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
                    "priority": 0,
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
                    "external_id": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "lom_educational_levels": [
                "HBO"
            ],
            "disciplines": [
                "aarde_milieu"
            ],
            "study_vocabulary": [],
            "technical_type": "document",
            "technical_types": [],
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": None,
            "metrics": None
        })

    def test_research_product_biology(self):
        data = generate_nl_product(topic="biology")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "entity": "products",
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Onderzoek over biologisch denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": [],
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
                    "priority": 0,
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
                    "external_id": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "sia_project_id": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "type": "document",
            "types": [],
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
                    "external_id": None,
                    "is_external": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                }
            ],
            "metrics": None
        })

    def test_learning_material_math_all_languages(self):
        data = generate_material(topic="math")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "entity": "products",
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Didactiek van wiskundig denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": ["cc-by-40"],
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
                    "priority": 0,
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
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "external_id": None,
                    "is_external": None
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
            "technical_types": ["document"],
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": "SURF",
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "metrics": {
                "views": 1,
                "stars": {
                    "average": 5.0,
                    "star_1": 0,
                    "star_2": 0,
                    "star_3": 0,
                    "star_4": 0,
                    "star_5": 1
                }
            },
        })

    def test_learning_material_biology_all_languages(self):
        data = generate_material(topic="biology")
        learning_material = LearningMaterial(**data)
        learning_material_json = learning_material.model_dump_json()
        learning_material_dump = json.loads(learning_material_json)
        self.assertEqual(learning_material_dump, {
            "entity": "products",
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Didactiek van biologisch denken",
            "description": "Materiaal voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": ["cc-by-40"],
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
                    "previews": None,
                    "priority": 0
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "lom_educational_levels": [
                "HBO"
            ],
            "disciplines": [
                "aarde_milieu"
            ],
            "study_vocabulary": [],
            "technical_type": "document",
            "technical_types": ["document"],
            "material_types": [],
            "aggregation_level": None,
            "publishers": [
                "Wikiwijs Maken"
            ],
            "consortium": None,
            "metrics": None
        })

    def test_research_product_math_all_languages(self):
        data = generate_product(topic="math")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "entity": "products",
            "srn": "sharekit:edusources:3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "set": "sharekit:edusources",
            "external_id": "3522b79c-928c-4249-a7f7-d2bcb3077f10",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://surfsharekit.nl/objectstore/949e22f3-cd66-4be2-aefd-c714918fe90e",
            "title": "Onderzoek over wiskundig denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "wiskundedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": ["cc-by-40"],
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
                        "preview_small": "https://surfpol-harvester-content-dev.s3.amazonaws.com/"
                                         "pdf-thumbnail-200x150.png"
                    },
                    "priority": 0
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                },
                {
                    "name": "Theo van den Bogaart",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                },
                {
                    "name": "Marc de Graaf",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [
                "nerds"
            ],
            "doi": "https://doi.org/10.12345",
            "sia_project_id": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "type": "document",
            "types": ["document"],
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
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "metrics": {
                "views": 1,
                "stars": {
                    "average": 5.0,
                    "star_1": 0,
                    "star_2": 0,
                    "star_3": 0,
                    "star_4": 0,
                    "star_5": 1
                }
            },
        })

    def test_research_product_biology_all_languages(self):
        data = generate_product(topic="biology")
        research_product = ResearchProduct(**data)
        research_product_json = research_product.model_dump_json()
        research_product_dump = json.loads(research_product_json)
        self.assertEqual(research_product_dump, {
            "entity": "products",
            "srn": "edurep:wikiwijsmaken:wikiwijsmaken:123",
            "set": "edurep:wikiwijsmaken",
            "external_id": "wikiwijsmaken:123",
            "state": "active",
            "provider": "Wikiwijs Maken",
            "score": 0.0,
            "published_at": "2017-04-16",
            "modified_at": None,
            "url": "https://maken.wikiwijs.nl/85927/Biologische_denkactiviteiten#!page-2454065",
            "title": "Onderzoek over biologisch denken",
            "description": "Onderzoek voor lerarenopleidingen en professionaliseringstrajecten gericht op "
                           "biologiedidactiek en ICT met Theo van den Bogaart",
            "language": "nl",
            "copyright": "cc-by-40",
            "licenses": ["cc-by-40"],
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
                    "previews": None,
                    "priority": 0
                }
            ],
            "authors": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "doi": None,
            "sia_project_id": None,
            "subtitle": None,
            "highlight": None,  # only gets added during actual search
            "type": "document",
            "types": ["document"],
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
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "contacts": [
                {
                    "name": "Michel van Ast",
                    "email": None,
                    "external_id": None,
                    "dai": None,
                    "isni": None,
                    "orcid": None,
                    "is_external": None
                }
            ],
            "metrics": None
        })

    def test_research_product_deleted(self):
        deleted_data = {
            "doi": None,
            "set": "sharekit:nppo",
            "srn": "sharekit:nppo:437b4035-0f81-4a34-b835-2903d42921b1",
            "files": [],
            "state": "deleted",
            "title": None,
            "authors": [],
            "keywords": [],
            "sia_project_id": None,
            "language": None,
            "provider": None,
            "subtitle": None,
            "copyright": None,
            "has_parts": [],
            "is_part_of": [],
            "publishers": [],
            "description": None,
            "external_id": "437b4035-0f81-4a34-b835-2903d42921b1",
            "modified_at": None,
            "organizations": None,
            "publisher_date": None,
            "publisher_year": None,
            "technical_type": None,
            "copyright_description": None,
            "overwrite": None,
            "metrics": None,
            "study_vocabulary": [],
            "disciplines_normalized": [],
            "consortium": None,
            "industries": {},
            "sectors": {},
            "publisher_year_normalized": None,
            "harvest_source": "nppo",
            "url": None,
            "mime_type": None,
            "previews": None,
            "video": None,
            "studies": [],
            "disciplines": [],
            "material_types": ["unknown"],
            "aggregation_level": None,
            "lom_educational_levels": [],
            "projects": [],
            "research_themes": [],
            "research_object_type": None,
            "learning_material_disciplines_normalized": [],
            "study_vocabulary_terms": [],
            "text": None,
            "suggest_phrase": None,
            "suggest_completion": []
        }
        research_product = ResearchProduct(**deleted_data)
        research_product_dump = research_product.model_dump(mode="json")
        entity = research_product_dump.pop("entity")
        self.assertEqual(entity, "products")
        self.assertEqual(research_product_dump, {
            "srn": "sharekit:nppo:437b4035-0f81-4a34-b835-2903d42921b1",
            "set": "sharekit:nppo",
            "external_id": "437b4035-0f81-4a34-b835-2903d42921b1",
            "state": "deleted",
            "provider": None,
            "score": 0.0,
            "published_at": None,
            "modified_at": None,
            "url": None,
            "title": None,
            "description": None,
            "language": None,
            "copyright": None,
            "licenses": [],
            "video": None,
            "harvest_source": "nppo",
            "previews": None,
            "files": [],
            "authors": [],
            "has_parts": [],
            "is_part_of": [],
            "keywords": [],
            "sia_project_id": None,
            "doi": None,
            "subtitle": None,
            "highlight": None,
            "metrics": None,
            "type": None,
            "types": [],
            "research_object_type": None,
            "parties": [],
            "research_themes": [],
            "projects": [],
            "owners": [],
            "contacts": [],
        })
