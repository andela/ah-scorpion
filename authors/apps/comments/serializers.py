from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied
from ..comments.models import Comment
from ..articles.models import Article
from ..authentication.serializers import UserSerializer
from ..articles.serializers import ArticleSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        slug = self.context['request'].data.get('slug')
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        try:
            user = self.context['request'].user
        except self.context['request'].user.DoesNotExist:
            raise \
                PermissionDenied('Please log in first to perform this action')
        comment = Comment.objects.create(
            user=user,
            article=article,
            **validated_data
        )
        return comment
