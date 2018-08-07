from django.http import HttpResponse
from django.test import TestCase
from jwt import ExpiredSignatureError
from rest_framework.exceptions import AuthenticationFailed

from authors.apps.authentication.backends import JWTAuthentication


def activate(request, token):
    jwt_authentication = JWTAuthentication()
    try:
        identity = jwt_authentication.authenticate_credentials(token)
    except AuthenticationFailed as e:

        return HttpResponse(status=401, content=e)

    user = identity[0]
    if user is not None:
        # Check is the account is already active
        if user.is_active is True:
            return HttpResponse(status=401,
                                content='Activation link has been used!')

        user.is_active = True
        user.save()
        return HttpResponse(
            'Thank you for confirming your email address. '
            'Welcome to Authors\' Haven.')
    # User is not found
    else:
        return HttpResponse(status=401, content='Activation link is invalid!')
