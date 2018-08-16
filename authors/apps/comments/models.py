"""Define our database tables."""
from django.db import models
from ..authentication.models import User
from ..articles.models import Article


class Comment(models.Model):
    """Define the Comment table."""

    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, db_column='article')
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(
        User, related_name='comment_dislikes', blank=True)
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        default=None,
        null=True)

    class Meta:
        """Order by time created, the most recently created is at the top."""

        ordering = ('createdAt',)


class CommentHistory(models.Model):
    comment = models.TextField()
    parent_comment = models.ForeignKey(Comment,
                                       on_delete=models.CASCADE,
                                       db_column='parent_comment')
    date_created = models.DateTimeField(auto_now=True)
