from django.conf.urls import url
from . import account_activator
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

# App name for the namespace in Django 2.0.6
app_name = "authentication"

urlpatterns = [
    url(r'^users/?$', RegistrationAPIView.as_view(), name='reg'),
    url(r'^users/login/?$', LoginAPIView.as_view(), name='login'),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view(), name='current_user'),
    url(r'^activate/(?P<token>.+?)$',
        account_activator.activate,
        name='activate'),
]
