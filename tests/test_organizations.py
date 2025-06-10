from unittest import TestCase

from search_client.serializers import Organization
from search_client.test.factories import generate_organization


class TestOrganizationModel(TestCase):

    def test_dump_research_organization(self):
        data = generate_organization()
        organization = Organization(**data)
        self.assertEqual(organization.model_dump(mode="json"), {
            "srn": "sharekit:nppo:b843a11b-0194-4f29-8c69-e753552b4d7f",
            "name": "Nieuw samenwerkingsaanvraag 2",
            "ror": None,
            "score": 0,
            "is_root": None,
            "entity": "organizations",
            "set": "sharekit:nppo",
            "provider": "sharekit",
            "state": "active",
            "description": "Het vervolg op Nieuw Samenwerkingsaanvraag",
            "type": "consortium",
            "secretary": None,
            "parents": [],
            "members": []
        })
