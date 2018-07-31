from django.conf.urls import url
from . import account_activator
from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

# App name for the namespace in Django 2.0.6
app_name = "authentication"

urlpatterns = [
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^users/?$', RegistrationAPIView.as_view()),
    url(r'^users/login/?$', LoginAPIView.as_view()),
    url(r'^activate/(?P<token>.+?)$',
        account_activator.activate,
        name='activate'),
]
