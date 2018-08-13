from django.urls import path

from . import account_activator
from .views import (LoginAPIView, RegistrationAPIView,
                    UserRetrieveUpdateAPIView, ResetPasswordAPIView,
                    ConfirmResetPassword, ResetPasswordDoneAPIView, SocialAuth)

# App name for the namespace in Django 2.0.6
app_name = "authentication"

urlpatterns = [
    path('users/signup/', RegistrationAPIView.as_view(), name='reg'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='current_user'),
    path('activate/<str:token>', account_activator.activate, name='activate'),
    path(
        'reset-password/',
        ResetPasswordAPIView.as_view(),
        name='reset-password'),
    path(
        'confirm-password/<str:token>',
        ConfirmResetPassword.as_view(),
        name="password_reset_done"),
    path(
        'reset-password-done/',
        ResetPasswordDoneAPIView.as_view(),
        name='reset-password-done'),
    path('users/social_auth/', SocialAuth.as_view(), name="social_auth")
]
