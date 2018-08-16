from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied
from ..comments.models import Comment, CommentHistory
from ..articles.models import Article
from ..authentication.serializers import UserSerializer
from ..articles.serializers import ArticleSerializer


class CommentSerializer(serializers.ModelSerializer):
    """serialize data for handling comments."""

    user = UserSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)
    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    dislikes = serializers.SerializerMethodField(
        method_name='get_dislikes_count')

    class Meta:
        """specify the model and fields to be used by the serializer."""

        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        """Handle creating a new comment."""
        slug = self.context['request'].data.get('slug')
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        try:
            user = self.context['request'].user
        except self.context['request'].user.DoesNotExist:
            raise PermissionDenied(
                'Please log in first to perform this action')
        comment = Comment.objects.create(
            user=user, article=article, **validated_data)
        return comment

    def get_likes_count(self, instance):
        """Get the total number of likes for a particular comment."""
        return instance.likes.count()

    def get_dislikes_count(self, instance):
        """Get the total number of dislikes for a particular comment."""
        return instance.dislikes.count()


class CommentHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentHistory
        fields = '__all__'
