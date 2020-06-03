from django.test import TestCase
from django.test import Client


class TestCore(TestCase):

    def test_health(self):
        client = Client()
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['healthy'])