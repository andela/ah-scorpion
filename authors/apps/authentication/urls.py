from django.urls import path

from . import account_activator
from .views import (LoginAPIView, RegistrationAPIView,
                    UserRetrieveUpdateAPIView, ResetPasswordAPIView,
<<<<<<< HEAD
                    ConfirmResetPassword, ResetPasswordDoneAPIView, SocialAuth)
=======
                    ConfirmResetPassword, ResetPasswordDoneAPIView)
# reset_password_confirm))
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d

# App name for the namespace in Django 2.0.6
app_name = "authentication"

urlpatterns = [
<<<<<<< HEAD
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
    path('social_auth/', SocialAuth.as_view(), name="social_auth")
=======
    url(r'^users/?$', RegistrationAPIView.as_view(), name='reg'),
    url(r'^users/login/?$', LoginAPIView.as_view(), name='login'),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view(), name='current_user'),
    url(r'^activate/(?P<token>.+?)$',
        account_activator.activate,
        name='activate'),
    url(r'^reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    url(r'^confirm-password/(?P<token>.+?)$',
        ConfirmResetPassword.as_view(),
        name="password_reset_done"),
     url(r'^reset-password-done/',
       ResetPasswordDoneAPIView.as_view(), name='reset-password-done'),
>>>>>>> 6252091f7c17e7ffa9e1d9fb87ce196f3c34001d
]
