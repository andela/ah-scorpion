# articles/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

from authors.apps.articles.views import ArticleList, ArticleDetail, LikeArticle, DislikeArticle
from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.data = {
            "title": "Be a python coder in three weeks without a hassle",
            "description": "Are you ready?",
            "body": "It takes grit",
            "tagList": ["javscript", "python"],
            "images": ["image1", "image2"]
        }
        # Set up the registration url.
        self.articles_url = reverse('articles:all_articles')
        self.request_factory = APIRequestFactory()
        User.objects.create(
            username='olivia', email='olivia@gmail.com', password='1232444nm')

    def test_create_without_login(self):
        """
        Test that a user can't create an article without authorisation.
        """
        response = self.client.post(
            self.articles_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article_successfully(self):
        """
        Test that user can create article successfully
        """
        user = User.objects.get(username='olivia')
        view = ArticleList.as_view()
        request = self.request_factory.post(
            self.articles_url, self.data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_without_data(self):
        """
        Test that user can't create article without title
        """
        user = User.objects.get(username='olivia')
        view = ArticleList.as_view()
        request = self.request_factory.post(
            self.articles_url, {}, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_non_existent(self):
        """
        Test that user can't delete an article that does not exist
        """
        user = User.objects.get(username='olivia')
        view = ArticleDetail.as_view()
        url = reverse('articles:article_detail', kwargs={"slug": "not-found"})
        request = self.request_factory.delete(url)
        force_authenticate(request, user=user)
        response = view(request, slug="not-found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_non_existent(self):
        """
        Test that a user  can't update an article that does not exist
        """
        user = User.objects.get(username='olivia')
        view = ArticleDetail.as_view()
        url = reverse('articles:article_detail', kwargs={"slug": "not-found"})
        request = self.request_factory.put(url, self.data)
        force_authenticate(request, user=user)
        response = view(request, slug="not-found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_article_successful(self):
        """
        Test user can successfully update an article
        """
        user = User.objects.get(username='olivia')
        list_view = ArticleList.as_view()
        detail_view = ArticleDetail.as_view()
        create_request = self.request_factory.post(self.articles_url,
                                                   self.data)
        force_authenticate(create_request, user=user)
        create_response = list_view(create_request)
        slug = create_response.data['slug']
        url = reverse('articles:article_detail', kwargs={"slug": slug})
        update_request = self.request_factory.put(url, self.data)
        force_authenticate(update_request, user=user)
        update_response = detail_view(update_request, slug=slug)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    def test_delete_article_successful(self):
        """
        Test user can successfully delete an article
        """
        user = User.objects.get(username='olivia')
        list_view = ArticleList.as_view()
        detail_view = ArticleDetail.as_view()
        create_request = self.request_factory.post(self.articles_url,
                                                   self.data)
        force_authenticate(create_request, user=user)
        create_response = list_view(create_request)
        slug = create_response.data['slug']
        url = reverse('articles:article_detail', kwargs={"slug": slug})
        update_request = self.request_factory.delete(url)
        force_authenticate(update_request, user=user)
        update_response = detail_view(update_request, slug=slug)
        self.assertEqual(update_response.status_code,
                         status.HTTP_204_NO_CONTENT)


class LikeDislikeTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        data = {
            "title": "Be a python coder in three weeks without a hassle",
            "description": "Are you ready?",
            "body": "It takes grit",
            "tagList": ["javscript", "python"],
            "images": ["image1", "image2"]
        }

        articles_url = reverse('articles:all_articles')
        self.request_factory = APIRequestFactory()
        User.objects.create(
            username='olivia', email='olivia@gmail.com', password='1232444nm')

        view = ArticleList.as_view()
        user = User.objects.get(username='olivia')
        request = self.request_factory.post(articles_url, data, format='json')
        force_authenticate(request, user=user)
        response = view(request)
        self.slug = response.data["slug"]

        # set up like and dislike urls
        self.likes_url = reverse('articles:like_article', args=[self.slug])
        self.dislikes_url = reverse(
            'articles:dislike_article', args=[self.slug])

    def test_like_without_auth(self):
        """
        Test that a user can't like an article without authorization.
        """
        response = self.client.put(self.likes_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dislike_without_auth(self):
        """
        Test that a user can't dislike an article without authorization.
        """
        response = self.client.put(self.dislikes_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_like(self):
        """
        Test that user can like an article successfully
        """
        user = User.objects.get(username='olivia')
        view = LikeArticle.as_view()
        request = self.request_factory.put(self.likes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["Message"],
                      'You have successfully liked this article')

    def test_successful_unlike(self):
        """
        Test that user can unlike an article successfully
        """
        user = User.objects.get(username='olivia')
        view = LikeArticle.as_view()

        # first request
        request = self.request_factory.put(self.likes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)

        # second request
        request = self.request_factory.put(self.likes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["Message"],
                      'You no longer like this article')

    def test_successful_dislike(self):
        """
        Test that user can dislike an article successfully
        """
        user = User.objects.get(username='olivia')
        view = DislikeArticle.as_view()
        request = self.request_factory.put(self.dislikes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["Message"],
                      'You have successfully disliked this article')

    def test_successful_undislike(self):
        """
        Test that user can undislike an article successfully
        """
        user = User.objects.get(username='olivia')
        view = DislikeArticle.as_view()

        # first request
        request = self.request_factory.put(self.dislikes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)

        # second request
        request = self.request_factory.put(self.dislikes_url, args=[self.slug])
        force_authenticate(request, user=user)
        response = view(request, slug=self.slug)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data["Message"],
                      'You no longer dislike this article')
