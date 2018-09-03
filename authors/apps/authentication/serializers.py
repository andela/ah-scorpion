import re

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authors.apps.core.e_mail import SendEmail
from authors.settings import EMAIL_HOST_NAME, RESET_DOMAIN
from .models import User


def password_validator(password):
    password_pattern = re.compile(r"(?=^.{8,80}$)(?=.*\d)"
                                  r"(?=.*[a-z])(?!.*\s).*$")
    if not bool(password_pattern.match(password)):
        raise serializers.ValidationError(
            "Password invalid. Password must be 8 characters long, "
            "include numbers and letters and have no spaces"
        )
    return password


def password_validator(password):
    password_pattern = re.compile(r"(?=^.{8,80}$)(?=.*\d)"
                                  r"(?=.*[a-z])(?!.*\s).*$")
    if not bool(password_pattern.match(password)):
        raise serializers.ValidationError(
            "Password invalid. Password must be 8 characters long, "
            "include numbers and letters and have no spaces")
    return password


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        validators=[password_validator])
    email = serializers.EmailField(
        max_length=30,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=
                "Email already exists, please login or use a different email")
        ],
    )
    username = serializers.CharField(
        max_length=30,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=
                "Username already exists, please enter a different username")
        ],
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.

        # import generate_token
        # 'generate_token' is imported to prevent import error
        from authors.apps.core.token import generate_token
        from authors.apps.core.e_mail import SendEmail
        from django.contrib.sites.shortcuts import get_current_site
        from authors.settings import EMAIL_HOST_NAME

        email = SendEmail(
            mail_subject="Activate Authors' Haven account.",
            from_email=EMAIL_HOST_NAME,
            to=validated_data["email"],
            template='verification_email.html',
            content={
                'user': validated_data,
                'domain': get_current_site(self.context["request"]).domain,
                'token': generate_token(validated_data),
            })
        email.send()
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    bio = serializers.CharField(max_length=128, read_only=True)
    image = serializers.ImageField(max_length=254, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # As mentioned above, an email is required. Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.')

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')

        # Verify that the user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'email or password used is invalid')

        # Verify that the user is active
        if not user.is_active:
            raise serializers.ValidationError(
                'Please verify your email address to activate account')

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)
        # modified this method to return the User object

        if user is None:
            raise serializers.ValidationError(
                'email or password used is invalid')

        return user


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so let's just stick with the defaults.
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'bio', 'image')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is because
        # we don't need to specify anything else about the field. For the
        # password field, we needed to specify the `min_length` and
        # `max_length` properties too, but that isn't the case for the token
        # field.

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance


class ForgotPasswordSerializers(serializers.Serializer):
    # Ensure email is 255 character at maximum
    email = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=128, min_length=8, required=False)

    def validate(self, data):
        # validates and checks if the user exist in th database
        # if not raises a validation error

        user = User.objects.filter(email=data.get('email', None)).first()
        if user is None:
            raise serializers.ValidationError(
                'User with this email was not found')

        # genetate token for user
        token = default_token_generator.make_token(user)

        email = SendEmail(
            mail_subject="Confirmation of Password reset",
            from_email=EMAIL_HOST_NAME,
            to=data.get('email', None),
            template='reset_password.html',
            content={
                'user': data.get("email", None),
                'domain': RESET_DOMAIN,
                'token': token,
            })
        email.send()

        return {"email": data.get('email'), "token": token}


class ResetPasswordDoneSerializers(serializers.Serializer):
    # email is required to check the token
    new_password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)
    reset_token = serializers.CharField(max_length=128)
    email = serializers.CharField(max_length=255)

    def validate(self, data):
        user = User.objects.filter(email=data.get('email', None)).first()
        # check validity of the token against the user's email
        is_valid_token = default_token_generator.check_token(
            user, data.get('reset_token', None))

        if is_valid_token is not True:
            raise serializers.ValidationError(
                "Invalid token or Activation expired")

        user.set_password(data.get('new_password', None))
        user.save()
        return data


class SocialAuthSerializer(serializers.Serializer):
    """Serializers social_auth requests"""
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(
        max_length=1024, required=True, trim_whitespace=True)
