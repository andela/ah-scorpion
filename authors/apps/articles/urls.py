from django.urls import path, include

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
    path('<str:slug>/ratings',
         include('authors.apps.ratings.urls', namespace='ratings')),
    path(
        '<str:slug>/favorite/',
        views.FavoriteArticle.as_view(),
        name='article_favorite'),
]
