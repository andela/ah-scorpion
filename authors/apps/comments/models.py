from django.db import models
from ..authentication.models import User
from ..articles.models import Article


class Comment(models.Model):
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', default=None, null=True)

    class Meta:
        ordering = ('createdAt',)
