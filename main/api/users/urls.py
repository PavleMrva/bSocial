from django.conf.urls import url
from . import views
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
    Worker1TestAPIView,
    Worker2TestAPIView
)

app_name = 'user-api'

urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^wstest/$', Worker1TestAPIView.as_view(), name='wstest'),
    url(r'^rqtest/$', Worker2TestAPIView.as_view(), name='rqtest'),
]
