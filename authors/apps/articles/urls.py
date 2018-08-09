from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "articles"

urlpatterns = [
    path('', views.ArticleList.as_view(), name='all_articles'),
    path('<str:slug>/', views.ArticleDetail.as_view(), name='article_detail'),
    path('<str:slug>/like/', views.LikeArticle.as_view(), name='like_article'),
    path('<str:slug>/dislike/', views.DislikeArticle.as_view(), name='dislike_article'),
    path('<str:slug>/ratings', include('authors.apps.ratings.urls',
                                       namespace='ratings'))

]

urlpatterns = format_suffix_patterns(urlpatterns)
