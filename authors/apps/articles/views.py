import uuid

from django.utils.text import slugify
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
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
        slug_text = context["request"].data.get(
            "title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({"author": author, "slug": slug})
        return context


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ArticleDetail, self).get_serializer_context()
        author = context["request"].user.pk
        slug_text = context["request"].data.get(
            "title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({"author": author, "slug": slug})
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
        # nothing changes if the user does not exist in the list of
        # disliking users
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

class FavoriteArticle(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Add or removes a user and article to the list of users liking different
    articles.
    If the user has not already favourited an article, he is updated to
    favourite it
    Else: The use no longer favourites the article
    """

    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        """
        Helps user favourite article
        If already, return message saying that the user has already favourated
        Else make the user favourite article
        :param request:
        :param slug:
        :return: article
        ":return: response
        """
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            response = {"message": "The article was not found", }
            return Response(response,
                            status=status.HTTP_404_NOT_FOUND)
        user = request.user

        if user in article.favorited.all():
            # Returns a message that the user has already favourited article

            response = {
                "message": "You have already marked "
                           "this article as a favourite"}
            return Response(response, status=status.HTTP_200_OK)

        else:
            # Add user from the list of users liking the particular article
            article.favorited.add(user.id)

            serializer = self.get_serializer(article)
            response = {"article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, slug):
        """
        Helps user un-favourite article
        If already, return article
        Else message saying that the user has not favourated article
        :param request:
        :param slug:
        :return: article
        ":return: response
        """

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            response = {"message": "The article was not found", }
            return Response(response,
                            status=status.HTTP_404_NOT_FOUND)
        user = request.user

        if user in article.favorited.all():
            # Remove user from the list of users liking the particular article
            article.favorited.remove(user.id)

            serializer = self.get_serializer(article)
            response = {"article": serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            # Returns a message that the user has already favourited article
            response = {
                "message": "You have not marked this article as a favourite"}
            return Response(response, status=status.HTTP_200_OK)
