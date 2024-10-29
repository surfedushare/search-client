from unittest import TestCase
import pytest

from pydantic import ValidationError

from search_client.serializers.persons import Contact


class TestContactModel(TestCase):

    def test_identifier_validation(self):
        with pytest.raises(ValidationError):
            Contact(email=None, external_id=None, name="John Doe")
        email_contact = Contact(email="johndoe@example.com", external_id=None, name=None)
        self.assertIsInstance(email_contact, Contact)
        id_contact = Contact(email=None, external_id="test:person:1", name=None)
        self.assertIsInstance(id_contact, Contact)
