from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from .utility import TEST_USER, create_user
from rest_framework import status
from django.urls import reverse


class TestPasswordReset(APITestCase):
    """ Testcase for reset password"""

    EMAIL = {"email": "email@email.com"}

    def test_user_receive_reset_password_email(self):
        """ Test if user receives email. """
        create_user()
        response = self.client.post(
            reverse("authentication:reset-password"),
            self.EMAIL,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tes_update_password(self):
        """ Tests if the user can reset(update) their password. """
        user = create_user()
        token = default_token_generator.make_token(user)
        RESET_DATA = {
            "reset_data": {
                "token": token,
                "email": user.email,
                "new_password": "UpdatedPassword"
            }
        }

        response = self.client.put(
            reverse("authentication:reset-password-done"),
            RESET_DATA,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         "You have successfully reset your password")
