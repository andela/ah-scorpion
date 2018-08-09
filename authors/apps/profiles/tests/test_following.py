# authentication/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authors.apps.authentication.models import User


# Remove "user":
class FollowingTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.user_one = {
            "username": "Jacob",
            "email": "jake@jake.jake",
            "password": "jakejake23"
        }
        self.user_two = {
            "username": "sam",
            "email": "sam@jake.jake",
            "password": "jakejake23"
        }
        self.user_three = {
            "username": "zack",
            "email": "zack@jake.jake",
            "password": "jakejake23"
        }

        # Set up the registration url.
        self.reg_url = reverse('authentication:reg')
        # Register users to follow.
        reg_response = self.client.post(
            self.reg_url, self.user_two, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        # Make the user active by force authentication.
        self.force_authenticate('sam@jake.jake')
        # Second user.
        reg_response = self.client.post(
            self.reg_url, self.user_three, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        # Make the user active by force authentication.
        self.force_authenticate('zack@jake.jake')

    def force_authenticate(self, email):
        # Make the user active by authenticating in the model
        user = User.objects.filter(email=email).first()
        user.is_active = True
        user.save()

    def register_login_current_user(self):
        """
        Register, login and get token of current user
        """
        # Set up the registration and login url.
        self.reg_url = reverse('authentication:reg')
        self.login_url = reverse('authentication:login')
        # Register and login current user.
        reg_response = self.client.post(
            self.reg_url, self.user_one, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_201_CREATED)
        # Make the user active by authenticating in the model
        self.force_authenticate('jake@jake.jake')
        login_response = self.client.post(
            self.login_url, self.user_one, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_201_CREATED)
        token = 'Bearer ' + login_response.data['token']
        return token

    def test_user_following(self):
        """
        Test that a user can follow multiple users.
        """
        # Pass token of current user
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())
        # Follow the first user.
        follow_url = reverse('profiles:follow_user', args=['sam'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['username'], "sam")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Follow the second user.
        follow_url = reverse('profiles:follow_user', args=['zack'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['username'], "zack")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_unfollowing(self):
        """
        Test that a user can unfollow multiple users.
        """

        # Pass token of current user.
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())

        # Unfollow the first user.
        follow_url = reverse('profiles:follow_user', args=['sam'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['username'], "sam")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Unfollow the second user.
        follow_url = reverse('profiles:follow_user', args=['zack'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['username'], "zack")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_follow(self):
        """
        Test that an unauthorized user cannot follow multiple users.
        """
        # Follow the first user.
        follow_url = reverse('profiles:follow_user', args=['sam'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Follow the second user.
        follow_url = reverse('profiles:follow_user', args=['detail'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_cannot_unfollow(self):
        """
        Test that an unauthorized user cannot unfollow multiple users.
        """
        # Unfollow the first user.
        follow_url = reverse('profiles:follow_user', args=['sam'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Unfollow the second user.
        follow_url = reverse('profiles:follow_user', args=['detail'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['detail'],
                         "Authentication credentials were not provided.")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_follow_and_unfollow_themselves(self):
        """
        Test that a user can follow multiple users.
        """
        # Pass token of current user
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())
        # Follow themselves.
        follow_url = reverse('profiles:follow_user', args=['Jacob'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['errors'][0],
                         'You cannot follow yourself')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Unfollow themselves.
        follow_url = reverse('profiles:follow_user', args=['Jacob'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['errors'][0],
                         "You cannot unfollow yourself")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_follow_and_unfollow_non_existing_user(self):
        """
        Test that a user cannot follow and unfollow a non-existent user.
        """
        # Pass token of current user
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())
        # Follow a non-existent user.
        follow_url = reverse('profiles:follow_user', args=['ruth'])
        response = self.client.put(follow_url, format='json')
        self.assertEqual(response.data['detail'], 'Not found.')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Unfollow a non-existent user.
        follow_url = reverse('profiles:follow_user', args=['ruth'])
        response = self.client.delete(follow_url, format='json')
        self.assertEqual(response.data['detail'], "Not found.")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_view_followers(self):
        """
        Test that a user can view users they are following and their followers.
        """
        # Pass token of current user
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())
        # Check followers.
        followers_url = reverse('profiles:followers')
        response = self.client.get(followers_url, format='json')
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_view_following(self):
        """
        Test that a user can view users they are following.
        """
        # Pass token of current user
        self.client.credentials(
            HTTP_AUTHORIZATION=self.register_login_current_user())
        # Check following.
        following_url = reverse('profiles:following')
        response = self.client.get(following_url, format='json')
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
