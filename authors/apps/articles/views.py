from django.utils.text import slugify
import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Article
from .serializers import ArticleSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    # pagination_class = SetPagination

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
    permission_classes = (IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super(ArticleDetail, self).get_serializer_context()
        author = context["request"].user.pk
        slug_text = context["request"].data.get(
            "title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({"author": author, "slug": slug})
        return context
