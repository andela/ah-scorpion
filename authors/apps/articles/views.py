from django.utils.text import slugify
import uuid
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
    print("We are *****????")

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


class FavoriteArticle(generics.UpdateAPIView):
    """
    Add or removes a user and article to the list of users liking different
    articles.
    If the user has not already favourited an article, he is updated to
    favourite it
    Else: The use no longer favourites the article
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def update(self, request, slug):

        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            response = {"message": "The article was not found", }
            return Response(response,
                            status=status.HTTP_404_NOT_FOUND)

        user = request.user
        print("Article = ", article)

        if user in article.favorited.all():
            # Remove user from the list of users liking the particular article
            article.favorited.remove(user.id)

            response = {"message": "This article is no longer your favourite"}
            return Response(response, status=status.HTTP_200_OK)
        else:
            # Add user from the list of users liking the particular article
            article.favorited.add(user.id)

            response = {"message": "You have marked this article as your "
                                   "favourite"}
            return Response(response, status=status.HTTP_200_OK)
