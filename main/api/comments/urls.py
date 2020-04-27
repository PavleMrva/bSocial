from django.conf.urls import url
from . import views
from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIView,
)

app_name = 'comment-api'

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='detail'),
]
