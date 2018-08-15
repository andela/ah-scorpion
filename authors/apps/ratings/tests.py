# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from authors.apps.authentication.models import User


class RatingsTestCase(APITestCase):
    def setUp(self):
        self.reader = self.create_user()
        self.author = self.create_user(
            email='author@email.com',
            username='author',
        )
        self.slug = self.create_article().data['slug']
        self.client = APIClient()

    @staticmethod
    def create_user(email: str = 'test@email.com',
                    username: str = 'testuser',
                    password: str = 'password12345'):
        """
        Create an active user in the database
        :return: user
        """
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_active = True
        user.save()
        return user

    def login(self, user: User):
        """
        Login the user
        :return: token
        """
        login_url = reverse("authentication:login")
        response = self.client.post(login_url, {
            "email": user.email,
            "password": "password12345"
        }, format='json')
        return response.data['token']

    def create_article(self):
        """
        Create an article in the database
        :return: article
        """
        create_article_url = reverse('articles:all_articles')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.login(self.author))
        response = self.client.post(create_article_url,
                                    data={
                                        "title": "First Article Title",
                                        "description": "A short description "
                                                       "that shows a little "
                                                       "about this article",
                                        "body": "This just a short body",
                                        "images": [],
                                        "tagList": [],
                                    },
                                    format='json')
        return response

    def get_ratings(self, user: User = None, is_authenticated: bool = False,
                    is_found: bool = True):
        """
        Get the ratings of an article using the server
        :param user: The user that should get the rating if is_authenticated
        is True
        :param is_authenticated: Whether or not the request should be made
        with an authenticated user
        :param is_found: Whether or not the article should be found by the
        server
        :return: tuple of the status code and a string representation of the
        response's data
        :rtype: tuple
        """
        if not user:
            user = self.reader
        if is_found:
            slug = self.slug
        else:
            slug = 'not-meant-to-be-found'

        ratings_url = reverse('articles:ratings:all_ratings', kwargs={
            "slug": slug})
        if is_authenticated:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' + self.login(user)
            )
            response = self.client.get(ratings_url)
            return response._container[0].decode(), response.status_code
        else:
            response = self.client.get(ratings_url)
            return response._container[0].decode(), response.status_code

    def rate(self, user: User = None, is_authenticated: bool = True,
             is_found: bool = True, stars: int = 5):
        """
        Put a rating to an article via the server
        :param user: The user that should get the rating if is_authenticated
        is True
        :param is_authenticated: Whether or not the request should be made
        with an authenticated user
        :param is_found: Whether or not the article should be found by the
        server
        :param stars: The number of stars to be rated with, defaults to 5
        :return: tuple of the status code and a string representation of the
        response's data
        :rtype: tuple
        """
        if not user:
            user = self.reader
        if is_found:
            slug = self.slug
        else:
            slug = 'not-meant-to-be-found'

        ratings_url = reverse('articles:ratings:all_ratings', kwargs={
            "slug": slug})
        if is_authenticated:
            self.client.credentials(
                HTTP_AUTHORIZATION='Bearer ' + self.login(user)
            )
            response = self.client.post(ratings_url,
                                        data={"stars": stars},
                                        format='json')
            return response._container[0].decode(), response.status_code
        else:
            response = self.client.post(ratings_url,
                                        data={"stars": stars},
                                        format='json')
            return response._container[0].decode(), response.status_code

    def test_get_ratings_anonymous(self):
        """
        Test that an anonymous user can view an article's ratings
        """
        data_string, status_code = self.get_ratings()
        self.assertIn('ratings', data_string)
        self.assertEqual(200, status_code)

    def test_get_ratings_authenticated(self):
        """
        Test that an authenticated user can view an article's ratings
        """
        data_string, status_code = self.get_ratings(is_authenticated=True)
        self.assertIn('ratings', data_string)
        self.assertEqual(200, status_code)

    def test_get_ratings_unavailable_article(self):
        """
        Test it raises an error when an article is not found
        """
        data_string, status_code = self.get_ratings(is_found=False)
        self.assertIn('error', data_string)
        self.assertEqual(404, status_code)

    def test_rate_article_anonymous(self):
        """
        Test that an anonymous user cannot rate an article
        """
        data_string, status_code = self.rate(is_authenticated=False)
        self.assertIn('error', data_string)
        self.assertEqual(401, status_code)

    def test_rate_article_authenticated(self):
        """
        Test that an authenticated user can rate an article
        """
        data_string, status_code = self.rate()

        self.assertIn('ratings', data_string)
        self.assertEqual(201, status_code)
        self.assertIn('user', data_string)
        self.assertIn('stars', data_string)

        data_string, status_code = self.rate(stars=4)
        self.assertIn('4', data_string)

        data_string, status_code = self.rate(stars=40)
        self.assertEqual(400, status_code)
        self.assertIn('Star ratings should be from 1 and 5 stars', data_string)

        data_string, status_code = self.rate(stars=4000000000000)
        self.assertEqual(400, status_code)
        self.assertIn('Ensure this value is less than or equal to 32767.',
                      data_string)

    def test_rate_unavailable_article(self):
        """
        Test that when an article is not found an error is displayed
        """
        data_string, status_code = self.rate(is_found=False)
        self.assertIn('not found', data_string)
        self.assertEqual(400, status_code)

    def test_rate_my_own_article(self):
        """
        Test that an author cannot rate their own article
        """
        data_string, status_code = self.rate(user=self.author)
        self.assertIn('You cannot rate your own article', data_string)
        self.assertEqual(400, status_code)

    def test_that_articles_show_ratings(self):
        """
        Test that while getting an article, there are averageRating and
        ratingsCount
        """

        one_article_url = reverse("articles:article_detail",
                                  kwargs={"slug": self.slug})
        self.assertDictContainsSubset({"averageRating": None,
                                       "ratingsCount": 0},
                                      self.client.get(one_article_url).data)
