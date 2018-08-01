from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(
            queryset=Article.objects.all(),
            message="Title already exists, please enter a different Title")],
    )

    title = serializers.CharField(
        required=True,
        max_length=100,
    )

    class Meta:
        model = Article
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
