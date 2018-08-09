from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path('', views.RatingsRetrieveAPIView.as_view(), name='all_ratings'),
]
