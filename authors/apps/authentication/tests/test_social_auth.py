from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from unittest.mock import patch
from ..models import User


class SocialAuthenticationTests(APITestCase):
    def setUp(self):
        """
        Setup for tests
        """
        # Set up the social_auth url.
        self.auth_url = reverse('authentication:social_auth')

        self.client = APIClient()

        self.user = User(
            username='lenny',
            email='lennykmutua@gmail.com',
            password='123qwerty',
            is_active=True)
        self.user.save()

    def test_missing_access_token(self):
        """
        Test request without passing the access token
        """
        data = {"provider": "google-oauth2"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_provider(self):
        """
        Test request without passing the provider
        """
        access_token = "EAAexjwrTz4IBAC2T3cPCtLdLS3fUGVEz9Ma37"
        data = {"access_token": access_token}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_provider(self):
        """
        Test giving a non-existent provider
        """
        access_token = "EAAexjwrTz4IBAC2T3cPCtLdLS3fUGVEz9Ma37"
        data = {"access_token": access_token, "provider": "facebook-oauth23"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_token(self):
        """
        Test an invalid access token
        """
        access_token = "Invalid token"
        data = {"access_token": access_token, "provider": "facebook"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 400)

    @patch('authors.apps.authentication.views.load_backend')
    def test_valid_authentication(self, mock_backend):
        """
        Test a successful user authentication using social_auth
        """
        mock_backend().do_auth.return_value = self.user
        access_token = "AAexjwrTz4IBAC2T3cPCtLdLS3fUGVEz9Ma37"
        data = {"access_token": access_token, "provider": "facebook"}
        response = self.client.post(self.auth_url, data=data)
        self.assertEqual(response.status_code, 200)
