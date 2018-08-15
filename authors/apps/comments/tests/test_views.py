# articles/tests/test_views.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.comments.views import CommentsCreateDeleteAPIView
from authors.apps.comments.views import CommentsListCreateAPIView
from authors.apps.articles.views import ArticleList


class CommentsTests(APITestCase):
    def setUp(self):
        """
        Data for the tests
        """
        self.sample_comment = {
            "content": "This is a sample comment used for testing?"
        }
        self.sample_article = {
            "title": "Be a python coder in three weeks without a hassle",
            "description": "Are you ready?",
            "body": "It takes grit",
            "tagList": ["javscript", "python"],
            "images": ["image1", "image2"]
        }

        # Set up the registration url.
        self.articles_url = reverse('articles:all_articles')
        self.request_factory = APIRequestFactory()
        User.objects.create(username='olivia', email='olivia@gmail.com',
                            password='1232444nm')
        self.user = User.objects.get(username='olivia')
        self.article_view = ArticleList.as_view()
        self.comment_view = CommentsListCreateAPIView.as_view()
        self.article_request = self.request_factory.post(self.articles_url,
                                                         self.sample_article,
                                                         format='json')
        force_authenticate(self.article_request, user=self.user)
        self.article_response = self.article_view(self.article_request)
        self.slug = self.article_response.data['slug']
        self.pk = self.article_response.data['id']
        self.comments_url = reverse('comments:all_comments',
                                    kwargs={"slug": self.slug})
        self.comment_request = self.request_factory.post(self.comments_url,
                                                         self.sample_comment,
                                                         format='json')
        force_authenticate(self.comment_request, user=self.user)
        self.comment_response = self.comment_view(self.comment_request,
                                                  slug=self.slug)

    def test_comment_without_login(self):
        """
        Test that a user can't comment without authorisation.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": self.slug})
        request = self.request_factory.post(url, data=self.sample_comment)
        response = comment_view(request, slug=self.slug)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_without_data(self):
        """
        Test that a user can't comment without data.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": self.slug})
        request = self.request_factory.post(url, data={}, format='json')
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_successful(self):
        """
        Test that a user can comment successfully.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": self.slug})
        request = self.request_factory.post(url, data=self.sample_comment,
                                            format='json')
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_child_successful(self):
        """
        Test that a user can reply to a comment successfully.
        """
        pk = self.comment_response.data['id']
        comment_view = CommentsCreateDeleteAPIView.as_view()
        url = reverse('comments:comment_detail',
                      kwargs={"slug": self.slug, "pk": pk})
        request = self.request_factory.post(url, data=self.sample_comment,
                                            format='json')
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_child_without_parent(self):
        """
        Test that a user can't reply to a non-existent comment.
        """
        comment_view = CommentsCreateDeleteAPIView.as_view()
        url = reverse('comments:comment_detail',
                      kwargs={"slug": self.slug, "pk": "5463"})
        request = self.request_factory.post(url, data=self.sample_comment,
                                            format='json')
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug, pk="5463")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_without_article(self):
        """
        Test that a user can't comment on a non-existent article.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": '1234what'})
        request = self.request_factory.post(url, data=self.sample_comment,
                                            format='json')
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug='1234what')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_from_article_without_comment(self):
        """
        Test that a user can't get comment an article without comment.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": 'not'})
        request = self.request_factory.get(url)
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug='not')
        self.assertEqual(response.data, [])

    def test_get_comments_successful(self):
        """
        Test that a user can get comments successfully.
        """
        comment_view = CommentsListCreateAPIView.as_view()
        url = reverse('comments:all_comments', kwargs={"slug": self.slug})
        request = self.request_factory.get(url)
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug)
        self.assertIsInstance(response.data, list)
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_non_existent(self):
        """
        Test that a user can't delete non-existent comment
        """
        comment_view = CommentsCreateDeleteAPIView.as_view()
        url = reverse('comments:comment_detail',
                      kwargs={"slug": self.slug, "pk": "5463"})
        request = self.request_factory.delete(url)
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug, pk="5463")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment_successful(self):
        """
        Test that a user can delete comment
        """
        pk = self.comment_response.data['id']
        comment_view = CommentsCreateDeleteAPIView.as_view()
        url = reverse('comments:comment_detail',
                      kwargs={"slug": self.slug, "pk": pk})
        request = self.request_factory.delete(url)
        force_authenticate(request, user=self.user)
        response = comment_view(request, slug=self.slug, pk=pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
