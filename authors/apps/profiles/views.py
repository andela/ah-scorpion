# Create your views here.
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from authors.apps.authentication.models import User
from authors.apps.profiles.renderers import ProfileJSONRenderer
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
