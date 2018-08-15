from rest_framework import serializers

from .models import Article
from ..authentication.serializers import UserSerializer


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=True,
        max_length=100,
    )
    author = UserSerializer(read_only=True)

    likes = serializers.SerializerMethodField(method_name='get_likes_count')
    dislikes = serializers.SerializerMethodField(
        method_name='get_dislikes_count')
    favorited = serializers.SerializerMethodField(
        method_name='get_favorite_count')

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

    # These are important for displaying the ratings
    averageRating = serializers.SerializerMethodField()
    ratingsCount = serializers.SerializerMethodField()

    @staticmethod
    def get_averageRating(article):
        """
        Calculates weighted average rating.
        :param article: The article whose ratings we are calculating
        :return: None if no one has rated, The weighted average to 2 decimal
        places
        :rtype: float or None
        """
        all_ratings = article.ratings.all().count()
        fives = article.ratings.filter(stars=5).count()
        fours = article.ratings.filter(stars=4).count()
        threes = article.ratings.filter(stars=3).count()
        twos = article.ratings.filter(stars=2).count()
        ones = article.ratings.filter(stars=1).count()

        if all_ratings < 1:
            return None
        else:
            weighted_total = (5 * fives) + (4 * fours) + (3 * threes) + (
                        2 * twos) + (1 * ones)
            weighted_average = weighted_total / all_ratings
            return round(weighted_average, 2)

    @staticmethod
    def get_ratingsCount(article):
        """
        Method for getting the number of people who have rated.
        :param article: The article to be rated
        :return:
        :rtype: int
        """
        return article.ratings.all().count()

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

    @staticmethod
    def get_favorite_count(instance):
        """
        Gets the number of times that a particular article has been
        favourited
        """
        return instance.favorited.count()
