from django.http import HttpResponse
from authors.apps.authentication.backends import JWTAuthentication


def activate(request, token):
    jwt_authentication = JWTAuthentication()
    identity = jwt_authentication.authenticate_credentials(token)
    user = identity[0]

    if user is not None:
        # Check is the account is already active
        if user.is_active is True:
            return HttpResponse('Activation link has been used!')

        user.is_active = True
        user.save()
        return HttpResponse(
            'Thank you for confirming your email address. '
            'Welcome to Authors\' Haven.')
    # User is not found
    else:
        return HttpResponse('Activation link is invalid!')
