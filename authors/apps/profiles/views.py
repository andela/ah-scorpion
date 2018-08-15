# Create your views here.
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from authors.apps.authentication.models import User
from authors.apps.profiles.renderers import ProfileJSONRenderer, \
    FollowersJSONRenderer, FollowingJSONRenderer
from authors.apps.profiles.serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    """
    This class get's the user's profile from the database according to the
    username given in the URL
    """
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = ("username")


class FollowUserRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    """
    This class updates the follow table when a one user follows/unfollows
    another.
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = ("username")

    def update(self, request, username):
        """
        Method used in following users
        """
        current_user = self.request.user
        followed_user = self.get_object()
        # A user cannot follow themselves.
        if current_user == followed_user:
            raise ValidationError('You cannot follow yourself')
        # Follow the user in the follow field/join table.
        current_user.follows.add(followed_user)
        current_user.save()
        serializer = self.get_serializer(followed_user)
        return Response(serializer.data)

    def destroy(self, request, username):
        """
        Method used in unfollowing users
        """
        current_user = self.request.user
        unfollowed_user = self.get_object()
        # A user cannot unfollow themselves.
        if current_user == unfollowed_user:
            raise ValidationError('You cannot unfollow yourself')
        # unfollow the user in the follow field/join table.
        current_user.follows.remove(unfollowed_user)
        current_user.save()
        serializer = self.get_serializer(unfollowed_user)
        return Response(serializer.data)


class FollowersListAPIView(ListAPIView):
    """
    This class gets a user's followers and those he/she is following
    """
    renderer_classes = (FollowersJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        This view should return a list of all the followers
        for the currently authenticated user.
        """
        return self.request.user.followers


class UserFollowingListAPIView(ListAPIView):
    """
    This class gets a user's followers and those he/she is following
    """
    renderer_classes = (FollowingJSONRenderer,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        This view should return a list of all the followers
        for the currently authenticated user.
        """
        return self.request.user.follows
