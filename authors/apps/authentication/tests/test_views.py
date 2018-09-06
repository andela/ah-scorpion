# authentication/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.apps.authentication.models import User


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
        self.login_url = reverse('authentication:login')
        self.current_user_url = reverse('authentication:current_user')

    def test_register_user(self):
        """
        Test that a user can register.
        """
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['email'], self.data['email'])
        self.assertEqual(response.data['username'], self.data['username'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_without_user_name(self):
        """
        Test that a user cannot register without a username.
        """
        self.data['username'] = ""
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['errors']['username'][0],
                         "This field may not be blank.")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_empty_user_name(self):
        """
        Test that a user cannot register empty string.
        """
        self.data['username'] = " "
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['errors']['username'][0],
                         "This field may not be blank.")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weak_password(self):
        """
        Test that a user enters a password containing 8 characters
        with numbers and letters.
        """
        self.data['password'] = "1234"
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(
            response.data['errors']['password'][0],
            "Password invalid. Password must be 8 characters long,"
            " include numbers and letters and have no spaces")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_wrong_format(self):
        """
        Test that the user enters an email in the correct format
        """
        self.data['email'] = "jgmail"
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['errors']['email'][0],
                         "Enter a valid email address.")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_email(self):
        """
        Test that the user does not enter an empty email
        """
        self.data['email'] = ""
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.data['errors']['email'][0],
                         "This field may not be blank.")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_user(self):
        """
        Test that an already registered user cannot register again
        """
        test_user = {
            "username": "Jacob",
            "email": "jake@jake.jake",
            "password": "jakejake23"
        }

        # register the user the first time
        self.client.post(self.reg_url, test_user, format='json')

        # Register the user a second time
        response = self.client.post(self.reg_url, test_user, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """
        Test that a user can login
        """
        # Register a user
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(email=self.data['email']).first()
        user.is_active = True
        user.save()
        # Login the user
        login_response = self.client.post(
            self.login_url, {
                "email": "jake@jake.jake",
                "password": "jakejake23"
            },
            format='json')
        self.assertEqual(login_response.status_code, status.HTTP_201_CREATED)

    def test_login_user_wrong_email_and_password(self):
        """
        Test that you cannot login a user with the wrong email and password
        """
        # Register a user
        response = self.client.post(self.reg_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Login the user with wrong email
        login_response = self.client.post(
            self.login_url, {
                "email": "jake@.jake",
                "password": "jakejake23"
            },
            format='json')
        self.assertEqual(login_response.data['errors']['error'][0],
                         'email or password used is invalid')
        self.assertEqual(login_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        # Login the user with wrong password
        login_password_response = self.client.post(
            self.login_url, {
                "email": "jake@.jake",
                "password": "jake"
            },
            format='json')
        self.assertEqual(login_password_response.data['errors']['error'][0],
                         'email or password used is invalid')

        self.assertEqual(login_password_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_login_user_not_registered(self):
        """
        Test that a user who is not registered cannot login
        """
        login_response = self.client.post(
            self.login_url, {
                "email": "jake@.jake",
                "password": "jakejake23"
            },
            format='json')
        self.assertEqual(login_response.data['errors']['error'][0],
                         'email or password used is invalid')

        self.assertEqual(login_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_return_current_user(self):
        """
        Test that the current user can be returned.
        """
        # Register user.
        reg_response = self.client.post(self.reg_url, self.data, format='json')

        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        user = User.objects.filter(email=self.data['email']).first()
        user.is_active = True
        user.save()
        login_response = self.client.post(
            self.login_url, self.data, format='json')
        # Get current user.
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                                login_response.data['token'])
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.data['email'], "jake@jake.jake")
        self.assertEqual(response.data['username'], "Jacob")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_current_user_without_token(self):
        """
        Test that the request cannot be made without a token
        """
        response = self.client.get(self.current_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
