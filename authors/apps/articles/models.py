from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..authentication.models import User


class Article(models.Model):
    """This is a model for storing articles in the database"""
    slug = models.CharField(max_length=200, null=True, blank=True, unique=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    description = models.CharField(max_length=100)
    images = ArrayField(
        models.CharField(max_length=1000, blank=True),
        size=20,
        null=True,
        blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    tagList = ArrayField(
        models.CharField(max_length=200), null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               db_column='author')

    favorited = models.ManyToManyField(User, related_name='favorited',
                                       blank=True)

    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='dislikes', blank=True)
    favorited = models.ManyToManyField(User, related_name='favorited',
                                       blank=True)

    def __str__(self):
        # IMPORTANT to distinguish between printing the title only and the
        # Article object itself
        return f'Article: <{self.title}>'

    class Meta:
        ordering = ('title',)
