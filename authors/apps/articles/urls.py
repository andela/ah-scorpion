from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "articles"

urlpatterns = [
    url(r'^$', views.ArticleList.as_view(), name='all_articles'),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view(), name='article_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
