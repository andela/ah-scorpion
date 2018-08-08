from django.utils.text import slugify
import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        context = super(ArticleList, self).get_serializer_context()
        author = context["request"].user.pk
        slug_text = context["request"].data.get("title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({
            "author": author,
            "slug": slug
        })
        return context


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ArticleDetail, self).get_serializer_context()
        author = context["request"].user.pk
        slug_text = context["request"].data.get("title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({
            "author": author,
            "slug": slug
        })
        return context


class LikeArticle(generics.UpdateAPIView):
    """
    Adds the user to the list of liking users and
    removes the user from the list of disliking users.
    If the user likes for a second time,
    we remove the user from the list of liking users
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, slug):
        article = Article.objects.get(slug=slug)
        user = request.user

        # removes the user from the list of disliking users,
        # nothing changes if the user does not exist in the list of disliking users
        article.dislikes.remove(user.id)

        # allows for the None option: you neither like nor dislike the article
        if user in article.likes.all():

            # removes the user from the list of liking users
            article.likes.remove(user.id)

            response = {"Message": "You no longer like this article"}
            return Response(response, status=status.HTTP_200_OK)

        # adds the user to the list of liking users
        article.likes.add(user.id)

        response = {"Message": "You have successfully liked this article"}
        return Response(response, status=status.HTTP_200_OK)


class DislikeArticle(generics.UpdateAPIView):
    """
    Adds the user to the list of disliking users and
    removes the user from the list of liking users.
    If the user dislikes for a second time,
    we remove the user from the list of disliking users
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, slug):
        article = Article.objects.get(slug=slug)
        user = request.user

        # removes the user from the list of liking users,
        # nothing changes if the user does not exist in the list of liking users
        article.likes.remove(user.id)

        # allows for the None option: you neither like nor dislike the article
        if user in article.dislikes.all():

            # removes the user from the list of disliking users
            article.dislikes.remove(user.id)

            response = {"Message": "You no longer dislike this article"}
            return Response(response, status=status.HTTP_200_OK)

        # adds the user to the list of disliking users
        article.dislikes.add(user.id)

        response = {"Message": "You have successfully disliked this article"}
        return Response(response, status=status.HTTP_200_OK)
