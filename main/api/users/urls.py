from django.conf.urls import url
from . import views
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    UserFollowingAPIView,
)

app_name = 'user-api'

urlpatterns = [
    url(r'^follow/$', UserFollowingAPIView.as_view(), name='follow'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
]
