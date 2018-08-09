from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        max_length=100,
    )

    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    dislikes = serializers.SerializerMethodField(
        method_name='get_dislikes_count')

    class Meta:
        model = Article
        fields = '__all__'
        lookup_url_kwarg = 'slug'

    def create(self, validated_data):
        return super().create(validated_data)

    def get_likes_count(self, instance):
        """
        Gets the total number of likes for a particular article
        """
        return instance.likes.count()

    def get_dislikes_count(self, instance):
        """
        Gets the total number of dislikes for a particular article
        """
        return instance.dislikes.count()
