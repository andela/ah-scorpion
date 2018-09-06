"""Define the urls of the comment app."""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "comments"

urlpatterns = [
    path('', views.CommentsListCreateAPIView.as_view(), name='all_comments'),
    path(
        '<int:pk>/',
        views.CommentsCreateDeleteAPIView.as_view(),
        name='comment_detail'),
    path('<int:pk>/like/', views.LikeComment.as_view(), name='like_comment'),
    path(
        '<int:pk>/dislike/',
        views.DislikeComment.as_view(),
        name='dislike_comment'),
    path(
        'history/<int:pk>/',
        views.GetCommentHistory.as_view(),
        name='comment_history'),
]
