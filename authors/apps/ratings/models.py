from django.db import models


class Rating(models.Model):
    user = models.ForeignKey('authentication.User',
                             on_delete=models.CASCADE, related_name="ratings")
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE,
                                related_name="ratings")
    stars = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Rating: <{self.user.username} - {self.stars}>'
