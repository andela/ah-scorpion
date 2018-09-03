from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed

from authors.apps.authentication.backends import JWTAuthentication
from authors.settings import FRONT_END_HOST_NAME


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
        front_end_host = FRONT_END_HOST_NAME
        front_end_host = front_end_host + "/login"
        return redirect(front_end_host)

    # User is not found
    else:
        return HttpResponse(status=401, content='Activation link is invalid!')
