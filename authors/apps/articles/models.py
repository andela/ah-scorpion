from django.db import models
from django.contrib.postgres.fields import ArrayField
from ..authentication.models import User


class Article(models.Model):
    slug = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    body = models.TextField()
    description = models.CharField(max_length=100)
    images = ArrayField(
        models.CharField(max_length=1000, blank=True),
        size=20,
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    tagList = ArrayField(models.CharField(max_length=200), blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
