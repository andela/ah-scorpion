# import jwt
#
# from django.conf import settings
#
# from rest_framework import authentication, exceptions
#
# from .models import User

"""Configure JWT Here"""


class JWTAuthentication:
    @staticmethod
    def authenticate(request):
        """
        To Implement authentication of received JWT
        :param request:
        :return:
        """
        pass

    @staticmethod
    def authenticate_header(request):
        pass

    pass
