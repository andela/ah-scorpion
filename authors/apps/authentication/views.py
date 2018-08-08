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
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin

from authors.apps.authentication.models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializers,
    RegistrationSerializer,
    UserSerializer,
    ResetPasswordDoneSerializers,
)
from authors.apps.core.token import generate_token
from authors.apps.core.e_mail import SendEmail


class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer


class LoginAPIView(CreateModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # pass 'perform_create' which saves object instance
        pass


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

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


class ResetPasswordAPIView(CreateModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny, )
    # renderer_classes = (UserJSONRenderer, )
    serializer_class = ForgotPasswordSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # pass 'perform_create' which saves object instance
        pass


class ConfirmResetPassword(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ForgotPasswordSerializers

    def list(self, request, token):
        # Displays the token.
        return Response({"token": token})


class ResetPasswordDoneAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ResetPasswordDoneSerializers

    def update(self, request):
        # updates the password
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {"Message": "You have successfully reset your password"}

        return Response(response, status=status.HTTP_201_CREATED)
