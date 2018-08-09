""" Module used to create user for testing. """
from django.contrib.auth import get_user_model

TEST_USER = {
    "email": "email@mail.com",
    "password": "Password123",
<<<<<<< HEAD
    "username": "User"
=======
    "username": "User",
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d
}


def create_user(username="User",
                email="email@email.com",
                password="Password123."):
    # create_user create and returns a user
    user = get_user_model().objects.create_user(
        username, email, password=password)
    user.save()
<<<<<<< HEAD
    return user
=======
    return user
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d
