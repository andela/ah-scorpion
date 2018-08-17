from django.utils.text import slugify
from django_filters import rest_framework as filters
from django.contrib.postgres.fields import ArrayField
import django_filters
import uuid

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


class ArticleFilter(filters.FilterSet):
    """
    Create a custom filter class for articles,
    for getting dynamic queries from the url
    """
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(
        field_name='description', lookup_expr='icontains')
    body = filters.CharFilter(field_name='body', lookup_expr='icontains')
    author__username = filters.CharFilter(
        field_name='author__username', lookup_expr='icontains')

    class Meta:
        """
        This class describes the fields to be used in the search.
        The ArrayField has also been over-ridden
        """
        model = Article
        fields = [
            'title', 'description', 'body', 'author__username', 'tagList'
        ]
        filter_overrides = {
            ArrayField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains', },
            },
        }


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ArticleFilter

    def get_serializer_context(self):
        context = super(ArticleList, self).get_serializer_context()
        request = context["request"]
        if not request:
            return context
        slug_text = context["request"].data.get(
            "title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({"slug": slug})
        return context


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ArticleDetail, self).get_serializer_context()
        try:
            url_slug = self.kwargs['slug']
        except Exception:
            raise NotFound('Please check your url')
        if context["request"].data.get(
                "title",
                "No Title") == Article.objects.get(slug=url_slug).title:
            slug = url_slug
        else:
            slug_text = context["request"].data.get(
                "title", "No Title") + " " + uuid.uuid4().hex
            slug = slugify(slug_text)
        context["request"].data.update({"slug": slug})
        return context


class LikeArticle(generics.UpdateAPIView):
    """
    Add the user to the list of liking users and
    remove the user from the list of disliking users.
    If the user likes for a second time,
    we remove the user from the list of liking users
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def update(self, request, slug):
        """Update the user's liking status on a particular article."""
        user = request.user

        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            raise NotFound('An article with this slug does not exist.')

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
    Add the user to the list of disliking users and
    remove the user from the list of liking users.
    If the user dislikes for a second time,
    we remove the user from the list of disliking users
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def update(self, request, slug):
        """Update the user's disliking status on a particular article."""
        user = request.user

        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            raise NotFound('An article with this slug does not exist.')

        # removes the user from the list of liking users,
        # nothing changes if the user does not exist in the  list of liking
        # users
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

    permission_classes = (IsAuthenticated, )
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        """
        Helps user favourite article
        If already, return message saying that the user has already favourited
        Else make the user favourite article
        :param request:
        :param slug:
        :return: article
        ":return: response
        """
        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                "message": "The article was not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        user = request.user

        if user in article.favorited.all():
            # Returns a message that the user has already favourited article

            response = {
                "message": "You have already marked "
                "this article as a favourite"
            }
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
        Else message saying that the user has not favourited article
        :param request:
        :param slug:
        :return: article
        ":return: response
        """

        try:
            article = Article.objects.get(slug=slug)
        except Exception:
            response = {
                "message": "The article was not found",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
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
                "message": "You have not marked this article as a favourite"
            }
            return Response(response, status=status.HTTP_200_OK)
