from rest_framework import serializers

from .models import Article
from ..authentication.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        max_length=100,
    )
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        lookup_url_kwarg = 'slug'

    def create(self, validated_data):
        author = self.context['request'].user
        article = Article.objects.create(
            author=author,
            **validated_data
        )
        return article
