import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.TokenAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            return None

        identity = jwt.decode(token, settings.SECRET_KEY)
        user = None
        try:
            user = User.objects.get(username=identity['username'])
        except User.DoesNotExist:
            exceptions.AuthenticationFailed('No such user')

        return user, None
