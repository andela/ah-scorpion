import requests
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy
from rest_framework.mixins import CreateModelMixin
from authors.apps.authentication.models import User
from authors.apps.core.token import generate_token
from .renderers import UserJSONRenderer, EmailJSONRenderer
from .serializers import (LoginSerializer, ForgotPasswordSerializers,
                          RegistrationSerializer, UserSerializer,
                          ResetPasswordDoneSerializers, SocialAuthSerializer)


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
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordAPIView(CreateModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (EmailJSONRenderer, )
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


class SocialAuth(generics.CreateAPIView):
    """
    Allow for social signup and login using Google and Facebook.
    """
    permission_classes = (AllowAny, )
    serializer_class = SocialAuthSerializer
    renderer_classes = (UserJSONRenderer, )

    def create(self, request):
        """
        Receive the access_token and provider from the request,
        once authentication is comlpete, create a new user record if it
        does not exist already. The user's information (username, email
        and image) are saved and the user is provided with a JWT token for
        authorization when using our API.
        """
        # Get the access_token and provider from request
        # the access_token is provided by the particular provider
        # which in our case is either 'google-oauth2' or 'facebook'
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider')
        access_token = serializer.data.get('access_token')

        # strategy sets up the required custom configuration for  working
        # with Django
        strategy = load_strategy(request)

        try:

            # Loads backends defined on SOCIAL_AUTH_AUTHENTICATION_BACKENDS,
            # checks the appropiate one by using the provider given
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)

        except MissingBackend:
            return Response(
                {
                    "errors": {
                        "provider": ["Invalid provider"]
                    }
                },
                status=status.HTTP_400_BAD_REQUEST)

        try:
            # authenticates the user and
            # creates a user in our user model if a user with
            # the given email and username does not exist already.
            # If the user exists, we just authenticate the user.
            user = backend.do_auth(access_token)

        except BaseException as error:
            return Response(
                {
                    "error": str(error),
                }, status=status.HTTP_400_BAD_REQUEST)

        # Since the user is using social authentication, there is no need
        # for email verification.
        # We therefore set the user to active here.
        if not user.is_active:
            user.is_active = True

        def get_image_url(self):
            """
            Get the user's current image url from the provider.
            save/update the image field of the particular user
            and returns the image_url.
            """
            try:
                if provider == "google-oauth2":
                    url = "http://picasaweb.google.com/data/entry/api/user/" \
                          "{}?alt=json".format(user.email)
                    data = requests.get(url).json()
                    image_url = data["entry"]["gphoto$thumbnail"]["$t"]

                elif provider == "facebook":
                    id_url = "https://graph.facebook.com/me?access_token={}" \
                        .format(access_token)
                    id_data = requests.get(id_url).json()
                    user_id = id_data["id"]
                    url = "http://graph.facebook.com/{}/picture?type=small" \
                        .format(user_id)
                    image_url = requests.get(url, allow_redirects=True).url

            except BaseException:
                image_url = ""

            user.image = image_url
            user.save()
            return image_url

        serializer = UserSerializer(user)
        output = serializer.data
        output['bio'] = serializer.instance.bio
        output['image'] = get_image_url(self)
        return Response(output, status=status.HTTP_200_OK)
