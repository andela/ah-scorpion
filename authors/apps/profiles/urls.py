from django.urls import path

from authors.apps.profiles.views import ProfileRetrieveAPIView
from authors.apps.profiles.views import FollowUserRetrieveAPIView

app_name = "profiles"

urlpatterns = [
    # url to view the profile of a user, does not require permissions
    path('<str:username>', ProfileRetrieveAPIView.as_view(),
         name='view_profile'),
    # Url to follow a user
    path('<str:username>/follow', FollowUserRetrieveAPIView.as_view(),
         name='follow_user'),
]
