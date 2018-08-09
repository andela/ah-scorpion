from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "articles"

urlpatterns = [
    path('', views.ArticleList.as_view(), name='all_articles'),
    path('<str:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('<str:slug>/like/', views.LikeArticle.as_view(), name='like_article'),
    path(
        '<str:slug>/dislike/',
        views.DislikeArticle.as_view(),
        name='dislike_article'),
    path('<str:slug>/favorite/', views.FavoriteArticle.as_view(),
         name='article_favorite'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
