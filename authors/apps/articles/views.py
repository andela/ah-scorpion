from django.utils.text import slugify
import uuid
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import NotFound

from .models import Article
from .serializers import ArticleSerializer


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_context(self):
        context = super(ArticleList, self).get_serializer_context()
        slug_text = context["request"].data.get("title", "No Title") + " " + uuid.uuid4().hex
        slug = slugify(slug_text)
        context["request"].data.update({
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
        try:
            url_slug = self.kwargs['slug']
        except self.kwargs.get('slug').DoesNotExist:
            raise NotFound('Please check your url')

        if context["request"].data.get("title", "No Title") == Article.objects.get(slug=url_slug).title:
            slug = url_slug
        else:
            slug_text = context["request"].data.get("title", "No Title") + " " + uuid.uuid4().hex
            slug = slugify(slug_text)
        context["request"].data.update({
            "slug": slug
        })
        return context
