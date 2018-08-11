# articles/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from authors.apps.comments.views import CommentsListCreateAPIView
from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.data = {

            "content": "How can I be a python coder in three weeks without a hassle?"

        }
        # Set up the registration url.
        self.comments_url = reverse('comments:all_comments')
        self.request_factory = APIRequestFactory()
        User.objects.create(username='olivia', email='olivia@gmail.com', password='1232444nm')




