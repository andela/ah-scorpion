""" Module used to create user for testing. """
from django.contrib.auth import get_user_model

TEST_USER = {
    "email": "email@mail.com",
    "password": "Password123",
    "username": "User",
}


def create_user(username="User",
                email="email@email.com",
                password="Password123."):
    # create_user create and returns a user
    user = get_user_model().objects.create_user(
        username, email, password=password)
    user.save()
    return user
