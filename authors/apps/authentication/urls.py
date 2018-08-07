from django.conf.urls import url
from django.urls import path
from . import account_activator
from .views import (LoginAPIView, RegistrationAPIView,
                    UserRetrieveUpdateAPIView, ResetPasswordAPIView,
                    ConfirmResetPassword, ResetPasswordDoneAPIView, SocialAuth)

# App name for the namespace in Django 2.0.6
app_name = "authentication"

urlpatterns = [
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
    path('social_auth/', SocialAuth.as_view(), name="social_auth")
]
