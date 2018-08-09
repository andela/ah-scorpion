from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from authors.apps.authentication.models import User


class ProfileTests(APITestCase):
    def setUp(self):
        """
        Set up
        """
        self.client = APIClient()

    def get_profile(self, username: str = 'username'):
        """
        Method for using the test client to send a get request to our API and
        return a response with the profile of a the given username
        :param username: the username to put into the URL
        :return: response as given by the API
        :rtype: Response
        """
        view_profile_url = reverse(
            'profiles:view_profile', args=[username])
        return self.client.get(view_profile_url)

    def test_user_views_profile_fail(self):
        """
        Test that a 404 is returned for trying to view a user that does not
        exist.
        """
        response = self.get_profile()
        self.assertEqual(404, response.status_code)
        self.assertIn('Not found', str(response.data))

    def test_user_views_profile_pass(self):
        """
        Test that anyone can view the profile of a registered user
        """
        # create user in the database
        user = User(
            email='rodger@rabbit.com',
            username='rodgerrabbit',
            password='password12345'
        )
        user.save()
        response = self.get_profile('rodgerrabbit')
        self.assertEqual(200, response.status_code)
        self.assertIn('rodgerrabbit', str(response.data))
        self.assertIn('bio', str(response.data))
        self.assertIn('image', str(response.data))
