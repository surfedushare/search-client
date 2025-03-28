from unittest import TestCase
import pytest

from pydantic import ValidationError

from search_client.serializers.persons import Contact, Researcher, Person
from search_client.test.factories.persons import generate_person


class TestContactModel(TestCase):

    def test_identifier_validation(self):
        with pytest.raises(ValidationError):
            Contact(email=None, external_id=None, name="John Doe")
        email_contact = Contact(email="johndoe@example.com", external_id=None, name=None)
        self.assertIsInstance(email_contact, Contact)
        id_contact = Contact(email=None, external_id="test:person:1", name=None)
        self.assertIsInstance(id_contact, Contact)


class TestResearcherModel(TestCase):

    def test_dump_researcher(self):
        data = generate_person()
        researcher = Researcher(**data)
        self.assertEqual(researcher.model_dump(mode="json"), {
            "entity": "persons",
            "srn": "sharekit:person:d5e05c12-0648-4129-9386-408d47b6f8c0",
            "set": "nppo",
            "provider": "sharekit",
            "state": "active",
            "score": 0.0,
            "name": "Brian May",
            "fist_name": None,
            "last_name": None,
            "prefix": None,
            "initials": None,
            "description": None,
            "email": None,
            "phone": None,
            "photo_url": None,
            "external_id": "d5e05c12-0648-4129-9386-408d47b6f8c0",
            "isni": None,
            "skills": [],
            "organizations": [],
            "is_employed": None,
            "job_title": None,
            "title": None,
            "themes": [
                "Queen"
            ],
            "orcid": None,
            "dai": None
        })


class TestPersonModel(TestCase):

    def test_dump_person(self):
        data = generate_person()
        person = Person(**data)
        self.assertEqual(person.model_dump(mode="json"), {
            "entity": "persons",
            "srn": "sharekit:person:d5e05c12-0648-4129-9386-408d47b6f8c0",
            "set": "nppo",
            "provider": "sharekit",
            "state": "active",
            "score": 0.0,
            "name": "Brian May",
            "fist_name": None,
            "last_name": None,
            "prefix": None,
            "initials": None,
            "description": None,
            "email": None,
            "phone": None,
            "photo_url": None,
            "external_id": "d5e05c12-0648-4129-9386-408d47b6f8c0",
            "isni": None,
            "skills": [],
            "organizations": [],
            "is_employed": None,
            "job_title": None,
        })
