import datetime
import jwt
import json
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.settings import SECRET_KEY, EMAIL_HOST_NAME
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializers,
    RegistrationSerializer,
    UserSerializer,
    ResetPasswordDoneSerializers,
)
from authors.apps.core.e_mail import SendEmail


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        current_site = get_current_site(request)
        mail_subject = "Activate Authors' Haven account."
        message = render_to_string(
            'verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': generate_token(user).decode(),
            })
        to_email = serializer.data.get("email")
        co_name = EMAIL_HOST_NAME

        email = EmailMessage(
            mail_subject, message, from_email=co_name, to=[to_email])
        email.send()

        output = serializer.data
        output['message'] = 'Please confirm your email address to complete ' \
                            'the registration '
        return Response(output, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        token = generate_token(serializer.data).decode()
        output = serializer.data
        output['token'] = token
        return Response(output, status=status.HTTP_200_OK)


def generate_token(identity: dict):
    """
    Method that generates a JSON Web Token for the user
    :param identity: User information to be encoded as a dictionary
    :return: JWT token
    :rtype: bytes
    """
    payload = dict(
        identity=identity,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(days=1))
    return jwt.encode(payload, SECRET_KEY)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = ForgotPasswordSerializers

    def post(self, request):
        email = request.data

        serializer = self.serializer_class(data=email)
        serializer.is_valid(raise_exception=True)

        email = SendEmail(
            mail_subject="Confirmation of Password reset",
            from_email=EMAIL_HOST_NAME,
            to=serializer.data.get('email'),
            template='reset_password.html',
            content={
                'user': email,
                'domain': get_current_site(request).domain,
                'token': serializer.data.get('token', None)
            })
        email.send()
        response = {
            "Message":
            "Please confirm your email address to complete your password reset"
        }

        return Response(response, status=status.HTTP_201_CREATED)


class ConfirmResetPassword(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = ForgotPasswordSerializers

    def get(self, request, token):
        # Displays the token.
        return Response({"token": token})


class ResetPasswordDoneAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPasswordDoneSerializers

    def put(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()

        output = serializer.data
        output['Message'] = "You have successfully reset your password"

        return Response(output, status=status.HTTP_201_CREATED)
