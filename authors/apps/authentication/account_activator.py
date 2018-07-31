import jwt
from django.contrib.auth.models import User as SuperUser
from django.http import HttpResponse
from rest_framework import exceptions

from authors import settings
from .models import User


def activate(request, token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        email_address = payload['identity']
    except jwt.exceptions.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Expired Token.')
    except jwt.exceptions.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token')

    try:
        user = User.objects.get(email=email_address)
    except(TypeError, ValueError, OverflowError, SuperUser.DoesNotExist):
        user = None

    if user is not None:
        # Check is the account is already active
        if user.is_active is True:
            return HttpResponse('Activation link has been used!')

        user.is_active = True
        user.save()
        return HttpResponse(
            'Thank you for confirming your email address. '
            'Welcome to Authors\' Haven.')
    else:
        return HttpResponse('Activation link is invalid!')
