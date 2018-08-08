from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        max_length=100,
    )

    class Meta:
        model = Article
        fields = '__all__'
        lookup_url_kwarg = 'slug'

    def create(self, validated_data):
        return super().create(validated_data)
