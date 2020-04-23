from django.conf.urls import url
from . import views
from .views import (
    PostCreateAPIView,
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
)
app_name = 'post-api'
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('users', views.UserView)
# router.register('posts', views.PostView)
# router.register('comments', views.CommentView)
# router.register('followings', views.UserFollowingView)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='list'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
    # path('', include(router.urls)),
    # path('register', registration_view, name="register")
]
