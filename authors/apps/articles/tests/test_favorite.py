from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, \
    APIRequestFactory

from authors.apps.articles.models import Article
from authors.apps.articles.views import FavoriteArticle
from authors.apps.authentication.models import User


class AuthenticationTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.title = "Be a python coder in three weeks without a hassle"

        self.user = {
            "username": "smunyili",
            "email": "musamo@live.com",
            "password": "1234Pass"
        }
        # Set up the registration url.
        self.login_url = reverse('authentication:login')
        self.reg_url = reverse('authentication:reg')
        self.activate_url = 'authentication:activate'
        self.request_factory = APIRequestFactory()
        self.articles_url = reverse('articles:all_articles')

        # Create a User
        user = User.objects.create(
            username='smunyili',
            email='musamo@live.com',
            password='1234Pass'
        )
        user.is_active = True
        user.save()

    def test_article_not_exist(self):
        user = User.objects.get(email="musamo@live.com")
        view = FavoriteArticle.as_view()
        favorite_url = 'articles:article_favorite'
        self.favorite_url = reverse(favorite_url,
                                    kwargs={"slug": 'This is not hjjdajdjsa'})
        request = self.request_factory.post(self.favorite_url)
        force_authenticate(request, user=user)

        response = view(request, 'This is not a valid slug')

        assert ("The article was not found" in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_favourite(self):
        user = User.objects.get(email="musamo@live.com")
        self.article = Article.objects.create(
            title="Be a python coder in three weeks without a hassle",
            description="Are you ready?",
            body="It takes grit",
            author=user,
            tagList=["javscript", "python"],
            images=["image1", "image2"]
        )
        slug = self.title + "jadjhjshnsanask"
        self.article.slug = slug
        self.article.save()

        view = FavoriteArticle.as_view()
        favorite_url = 'articles:article_favorite'

        self.favorite_url = reverse(favorite_url,
                                    kwargs={"slug": slug})
        request = self.request_factory.post(self.favorite_url)
        force_authenticate(request, user=user)

        response = view(request, slug)

        assert ("'title': 'Be a python coder in three weeks without a "
                "hassle'" and "'favorited': 1" in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        # Test trying to favourite again
        force_authenticate(request, user=user)
        response = view(request, slug)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        assert ("You have already marked this article as a favourite" in
                str(response.data))

    def test_un_favourite(self):
        user = User.objects.get(email="musamo@live.com")
        self.article = Article.objects.create(
            title="Be a python coder in three weeks without a hassle",
            description="Are you ready?",
            body="It takes grit",
            author=user,
            tagList=["javscript", "python"],
            images=["image1", "image2"]
        )
        slug = self.title + "jadjhjshnsanask"
        self.article.slug = slug
        self.article.save()

        view = FavoriteArticle.as_view()
        favorite_url = 'articles:article_favorite'

        self.favorite_url = reverse(favorite_url,
                                    kwargs={"slug": slug})
        request = self.request_factory.delete(self.favorite_url)

        # Test trying to un-favourite before favourite
        force_authenticate(request, user=user)

        response = view(request, slug)

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        assert ("You have not marked this article as a favourite" in
                str(response.data))

        # Favourite the article
        self.favorite_url = reverse(favorite_url,
                                    kwargs={"slug": slug})
        request = self.request_factory.post(self.favorite_url)
        force_authenticate(request, user=user)
        view(request, slug)

        # Un-favourite
        request = self.request_factory.delete(self.favorite_url)
        force_authenticate(request, user=user)
        response = view(request, slug)

        assert ("'title': 'Be a python coder in three weeks without a "
                "hassle'" and "'favorited': 0" in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
