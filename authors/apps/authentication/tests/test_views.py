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
        # Set up the registration url.
        self.reg_url = reverse('authentication:reg')

    def test_register_user(self):
        """
        Test that a user can register.
        """
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['email'], self.data['user']['email'])
        self.assertEqual(response.data['username'],
                         self.data['user']['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_without_user_name(self):
        """
        Test that a user cannot register without a username.
        """
        self.data['user']['username'] = ""
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(
            response.data['errors']['username'][0], "This field may not be blank.")

    def test_register_empty_user_name(self):
        """
        Test that a user cannot register empty string.
        """
        self.data['user']['username'] = " "
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(
            response.data['errors']['username'][0], "This field may not be blank.")

    def test_weak_password(self):
        """
        Test that a user enters a password containing 8 characters
        with numbers and letters.
        """
        self.data['user']['password'] = "1234"
        response = self.client.post(self.reg_url, self.data, format='json')
        print(response.data['errors']['password'][0])
        self.assertEqual(response.data['errors']['password'][0],
                         "Password invalid, Password must be 8 characters long, include numbers and letters and have no spaces")

    def test_email_wrong_format(self):
        """
        Test that the user enters an email in the correct format
        """
        self.data['user']['email'] = "jgmail"
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['errors']['email']
                         [0], "Enter a valid email address.")
