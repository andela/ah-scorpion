from django.urls import reverse
from rest_framework.test import APITestCase, APIClient


class SocialAuthenticationTests(APITestCase):


    def setUp(self):
        """
        Setup for tests
        """
        # Set up the social_auth url.
        self.auth_url = reverse('authentication:social_auth')

        self.client = APIClient()

    def test_missing_access_token(self):
        """
        Test request without passing the access token
        """
        data = {"provider" : "google-oauth2"}
        response = self.client.post(self.auth_url , data=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_provider(self):
        """
        Test request without passing the provider
        """
        access_token = "EAAexjwrTz4IBAC2T3cPCtLdLS3fUGVEz9Ma37"
        data = {"access_token" : access_token}
        response = self.client.post(self.auth_url , data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_provider(self):
        """
        Test giving a non-existent provider
        """
        access_token = "EAAexjwrTz4IBAC2T3cPCtLdLS3fUGVEz9Ma37"
        data = {"access_token" : access_token, "provider" : "facebook-oauth23"}
        response = self.client.post(self.auth_url , data=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_token(self):
        """
        Test an invalid access token
        """
        access_token = "Invalid token"
        data = {"access_token" : access_token, "provider" : "facebook"}
        response = self.client.post(self.auth_url , data=data)
        self.assertEqual(response.status_code, 400)
      