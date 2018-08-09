from django.urls import path

from authors.apps.profiles.views import ProfileRetrieveAPIView, UserFollowingListAPIView, FollowersListAPIView, FollowUserRetrieveAPIView

app_name = "profiles"

urlpatterns = [
    # url to view the profile of a user, does not require permissions
    path(
        '<str:username>',
        ProfileRetrieveAPIView.as_view(),
        name='view_profile'),
    path(
        '<str:username>/follow',
        FollowUserRetrieveAPIView.as_view(),
        name='follow_user'),
    path('following/', UserFollowingListAPIView.as_view(), name='following'),
    path('followers/', FollowersListAPIView.as_view(), name='followers'),
]
