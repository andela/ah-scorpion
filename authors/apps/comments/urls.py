from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = "comments"

urlpatterns = [
    path('', views.CommentsListCreateAPIView.as_view(), name='all_comments'),
    path('<int:pk>/', views.CommentsCreateDeleteAPIView.as_view(),
         name='comment_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
