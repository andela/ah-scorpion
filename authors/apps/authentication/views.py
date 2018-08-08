import datetime

import jwt
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from social_core.exceptions import MissingBackend
from social_django.utils import load_backend, load_strategy

from authors.apps.authentication.models import User
from authors.apps.core.e_mail import SendEmail
from authors.settings import SECRET_KEY, EMAIL_HOST_NAME
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializers,
    RegistrationSerializer,
    UserSerializer,
    ResetPasswordDoneSerializers,
    SocialAuthSerializer
)


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        current_site = get_current_site(request)
        mail_subject = "Activate Authors' Haven account."
        message = render_to_string('verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'token': generate_token(user),
        })
        to_email = serializer.data.get("email")
        co_name = EMAIL_HOST_NAME

        email = EmailMessage(
            mail_subject, message, from_email=co_name, to=[to_email])
        email.send()

        output = serializer.data
        output['message'] = 'Please confirm your email address to complete ' \
                            'the registration '

        # now that a user has been created and saved, the serializer's
        # instance attribute will be the created User object so we can get
        # the bio and image from it.
        output['bio'] = serializer.instance.bio
        output['image'] = serializer.instance.image

        return Response(output,
                        status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # generate token on login
        token = generate_token(serializer.data)
        output = serializer.data
        output['token'] = token

        # here serializer.instance returns None, so we use
        # serializer.validated_data which returns a user object
        output['bio'] = serializer.validated_data.bio
        output['image'] = serializer.validated_data.image
        return Response(output, status=status.HTTP_200_OK)


def generate_token(identity: dict, expiry: float = 86400):
    """
    Method that generates a JSON Web Token for the user
    :param identity: User information to be encoded as a dictionary
    :param expiry: Number of seconds the token should last
    :return: JWT token
    :rtype: string
    """
    payload = dict(
        identity=identity,
        iat=datetime.datetime.utcnow(),
        exp=datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry))
    return jwt.encode(payload, SECRET_KEY).decode()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
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


class ResetPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
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
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ForgotPasswordSerializers

    def get(self, request, token):
        # Displays the token.
        return Response({"token": token})


class ResetPasswordDoneAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordDoneSerializers

    def put(self, request):
        # updates the password
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = {"Message": "You have successfully reset your password"}

        return Response(response, status=status.HTTP_201_CREATED)


class SocialAuth(CreateAPIView):
    """
    Allows for social signup and login using Google and Facebook
    """
    permission_classes = (AllowAny,)
    serializer_class = SocialAuthSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """
        Receives the access_token and provider from the request,
        once authentication is comlpete, it creates a new user record
        if it does exist already. The user's information (username, email and image)
        are saved and the user is provided with a JWT token for authorization when
        using our API.
        """
        # Get the access_token and provider from request
        # the access_token is provided by the particular provider
        # which in our case is either 'google-oauth2' or 'facebook'
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.data.get('provider')
        access_token = serializer.data.get('access_token')

        # strategy sets up the required custom configuration for working with Django
        strategy = load_strategy(request)

        try:

            # Loads backends defined on SOCIAL_AUTH_AUTHENTICATION_BACKENDS,
            # checks the appropiate one by using the provider given
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)

        except MissingBackend:
            return Response({
                "errors": {
                    "provider": ["Invalid provider"]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # authenticates the user and 
            # creates a user in our user model if a user with
            # the given email and username does not exist already.
            # If the user exists, we just authenticate the user.
            user = backend.do_auth(access_token)

        except BaseException as error:
            return Response({
                "error": str(error),
            }, status=status.HTTP_400_BAD_REQUEST)

        # Since the user is using social authentication, there is no need
        # for email verification.
        # We therefore set the user to active here.
        if not user.is_active:
            user.is_active = True
            user.save()

        def get_image_url(self):
            """
            gets the user's current image url from the provider.
            saves/updates the image field of the particular user
            and returns the image_url
            """
            try:
                if provider == "google-oauth2":
                    url = "http://picasaweb.google.com/data/entry/api/user/{}?alt=json".format(
                        user.email)
                    data = requests.get(url).json()
                    image_url = data["entry"]["gphoto$thumbnail"]["$t"]

                elif provider == "facebook":
                    id_url = "https://graph.facebook.com/me?access_token={}".format(
                        access_token)
                    id_data = requests.get(id_url).json()
                    user_id = id_data["id"]
                    url = "http://graph.facebook.com/{}/picture?type=small".format(
                        user_id)
                    image_url = requests.get(url, allow_redirects=True).url

            except BaseException:
                image_url = ""

            user.image = image_url
            return image_url

        serializer = UserSerializer(user)
        token = generate_token(serializer.data)
        output = serializer.data
        output["token"] = token
        output['bio'] = serializer.instance.bio
        output['image'] = get_image_url(self)
        return Response(output, status=status.HTTP_200_OK)
