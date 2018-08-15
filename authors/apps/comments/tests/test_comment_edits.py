from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, \
    force_authenticate

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.comments.models import Comment
from authors.apps.comments.views import CommentsCreateDeleteAPIView, \
    GetCommentHistory


class CommentEditHistory(APITestCase):
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

        self.new_comment = {"content": "This is the new comment"}
        # Set up the registration url.

        self.request_factory = APIRequestFactory()
        self.update_comment_url = 'comments:comment_detail'
        self.get_comment_history_url = 'comments:comment_history'

        # Create a User
        user = User.objects.create(
            username='smunyili',
            email='musamo@live.com',
            password='1234Pass'
        )
        user.is_active = True
        user.save()

        self.user = User.objects.get(email="musamo@live.com")

        # Create a new article

        article = Article.objects.create(
            title="Be a python coder in three weeks without a hassle",
            description="Are you ready?",
            body="It takes grit",
            author=self.user,
            tagList=["javscript", "python"],
            images=["image1", "image2"]
        )
        self.slug = self.title + "2738-237923nwidh9223982392u0-66"
        article.slug = self.slug
        article.save()

        self.article = Article.objects.get(slug=self.slug)

        # Comment on the article
        comment = Comment.objects.create(
            content="This is a very nice comment",
            user=user,
            article=self.article
        )
        comment.save()
        self.comment = comment.pk

    def test_update_comment_not_found(self):
        view = CommentsCreateDeleteAPIView.as_view()

        self.update_comment_url = reverse(self.update_comment_url,
                                          kwargs={"slug": self.slug,
                                                  "pk": self.comment})
        request = self.request_factory.put(self.update_comment_url)
        force_authenticate(request, user=self.user)

        response = view(request, pk=8989090990)

        assert ("Comment not found" in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_comment_edited_successfully(self):
        view = CommentsCreateDeleteAPIView.as_view()

        self.update_comment_url = reverse(
            self.update_comment_url,
            kwargs={"slug": self.slug,
                    "pk": self.comment})
        request = self.request_factory.put(self.update_comment_url,
                                           data=self.new_comment,
                                           format='json')
        force_authenticate(request, user=self.user)

        response = view(request, pk=self.comment)

        assert (self.new_comment['content'] in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def test_duplicate_comment_rejected(self):
        view = CommentsCreateDeleteAPIView.as_view()

        self.update_comment_url = reverse(
            self.update_comment_url,
            kwargs={"slug": self.slug,
                    "pk": self.comment})
        request = self.request_factory.put(self.update_comment_url,
                                           data=self.new_comment,
                                           format='json')
        # Add the comment
        force_authenticate(request, user=self.user)
        view(request, pk=self.comment)

        # Try adding the same comment
        request = self.request_factory.put(self.update_comment_url,
                                           data=self.new_comment,
                                           format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=self.comment)

        assert ("New comment same as the existing. Editing rejected" in
                str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_comment_not_found(self):
        view = GetCommentHistory.as_view()

        self.get_comment_history_url = reverse(
            self.get_comment_history_url,
            kwargs={"slug": self.slug,
                    "pk": self.comment})
        request = self.request_factory.get(self.get_comment_history_url)
        force_authenticate(request, user=self.user)

        response = view(request, pk=8989898899)

        assert ("Comment not found" in str(response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_comment_history(self):

        # Create a comment
        view = CommentsCreateDeleteAPIView.as_view()
        self.update_comment_url = reverse(
            self.update_comment_url,
            kwargs={"slug": self.slug,
                    "pk": self.comment})
        request = self.request_factory.put(self.update_comment_url,
                                           data=self.new_comment,
                                           format='json')
        # Add the comment
        force_authenticate(request, user=self.user)
        view(request, pk=self.comment)

        view = GetCommentHistory.as_view()

        self.get_comment_history_url = reverse(
            self.get_comment_history_url,
            kwargs={"slug": self.slug,
                    "pk": self.comment})
        request = self.request_factory.get(self.get_comment_history_url)
        force_authenticate(request, user=self.user)

        response = view(request, pk=self.comment)

        assert (str(self.comment), self.new_comment['content'] in str(
            response.data))
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
