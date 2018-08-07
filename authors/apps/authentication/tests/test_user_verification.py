import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.views import generate_token


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.data = {
            "username": "Jacob",
            "email": "jake@jake.jake",
            "password": "jakejake23"
        }
        # Set up the registration url.
        self.reg_url = reverse('authentication:reg')
        self.activate_url = 'authentication:activate'

    def test_invalid_token_passed(self):
        """
        Tests if error 401 is returned if the activation URL is accessed
        with an invalid token
        :return: None
        """
        self.activate_url = reverse(self.activate_url,
                                    kwargs={'token': "hajshja"})
        response = self.client.get(
            self.activate_url)

        assert ("Invalid token" in str(response._container))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_expired_token_passed(self):
        """
        Tests if error 401 is returned if the activation URL is accessed
        with an expired token.
        A message 'Expired Token' should be sent to the browser using
        HTTPResponse
        :return: None
        """
        self.client.post(self.reg_url, self.data, format='json')
        token = generate_token(self.data['user'], 0.01).decode()
        time.sleep(2)

        self.activate_url = reverse(self.activate_url,
                                    kwargs={'token': token
                                            })
        response = self.client.get(
            self.activate_url)
        assert ("Expired Token" in str(response._container))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_valid_token_passed(self):
        """
        Tests if error 200 is returned if the activation URL is accessed
        with an valid token.
        A message 'Thank you for confirming your email address. '
            'Welcome to Authors' Haven.' should be sent to the browser using
        HTTPResponse
        :return: None
        """
        # register dummy user and get token
        response = self.client.post(self.reg_url, self.data, format='json')
        token = list(response.__dict__['context'])[0]["token"]

        self.activate_url = reverse(self.activate_url,
                                    kwargs={'token': token})
        response = self.client.get(
            self.activate_url)
        assert ("Thank you for confirming your email address" in str(
            response._container))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_used_token(self):
        """
        Tests if error 401 is returned if the activation URL is accessed
        with an valid token that has already been used.
        A message 'Activation link has been used!' should be sent to the browser
         using HTTPResponse
        :return: None
        """
        # register dummy user and get token
        response = self.client.post(self.reg_url, self.data, format='json')
        token = list(response.__dict__['context'])[0]["token"]
        self.activate_url = reverse(self.activate_url,
                                    kwargs={'token': token})

        # Verify the user
        self.client.get(
            self.activate_url)

        # Attempt using the token again
        response = self.client.get(
            self.activate_url)

        assert ("Activation link has been used!"
                in str(response._container))
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)
