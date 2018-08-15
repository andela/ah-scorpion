import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.TokenAuthentication):
    """
    Authenticate a received token from the 'Authorization' Header prepended by
    the keyword 'Bearer'

    Example
     Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZGVudGl0e
     SI6eyJlbWFpbCI6ImRhdmVtYXRoZXdzQGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiZGF2ZW1hd
     Ghld3MifSwiaWF0IjoxNTMyNDkyMjM2LCJleHAiOjE1MzI0OTIyNjZ9.
    """
    keyword = 'Bearer'

    def authenticate_credentials(self, token: str):
        """
        Check if the token is valid then authenticate the user
        :param token: the token as a string
        :return: Tuple of the user object and non-user authentication
        information
        :rtype: tuple
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Expired Token.')
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        identity = payload['identity']
        try:
            user = User.objects.get(username=identity['username'])
        except User.DoesNotExist:
            return None, None

        return user, None
