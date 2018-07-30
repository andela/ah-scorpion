# authentication/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.data = {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jakejake23"
            }
        }

    def test_register_user(self):
        """
        Test that a user can register.
        """
        url = reverse('authentication:reg')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.data['email'], self.data['user']['email'])
        self.assertEqual(response.data['username'],
                         self.data['user']['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
