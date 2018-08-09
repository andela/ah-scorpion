from django.utils.text import slugify
import uuid
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response

from authors.apps.profiles.renderers import ProfileJSONRenderer
from .models import Article
from .serializers import ArticleSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        context = super(ArticleList, self).get_serializer_context()
        author = context["request"].user.pk
        slug_text = context["request"].data.get("title",
                                                "No Title") + " " + uuid.uuid4().hex
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
        slug_text = context["request"].data.get("title",
                                                "No Title") \
                    + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({
            "author": author,
            "slug": slug
        })
        return context


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
        context = super(FavoriteArticle, self).get_serializer_context()
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

            response = {"article": context['request'].data}
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
        context = super(FavoriteArticle, self).get_serializer_context()

        user = request.user

        if user in article.favorited.all():
            # Remove user from the list of users liking the particular article
            article.favorited.remove(user.id)

            response = {"message": context['request'].data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            # Returns a message that the user has already favourited article
            response = {
                "message": "You have not already marked "
                           "this article as a favourite"}
            return Response(response, status=status.HTTP_200_OK)
