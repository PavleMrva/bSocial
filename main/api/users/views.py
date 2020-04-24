from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from djoser import email
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from rest_framework.views import APIView
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from main.api.posts.pagination import (
    PostLimitOffsetPagination,
    PostPageNumberPagination
)

from rest_framework.generics import (
    DestroyAPIView,
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    CreateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from main.api.posts.permissions import IsOwnerOrReadOnly

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)

from main.models import User


from django.http import JsonResponse

from django.views.generic.base import TemplateView


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_rq import job

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class UserCreateAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Worker1TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
        # message = RedisMessage('Hello World AAAAAAA MUUUUUUUUUUU')
        # # and somewhere else
        # redis_publisher.publish_message(message)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       "event": "New User",
                       "username": 'pavle'})

        return JsonResponse({'foo': 'bar'})


@job
def long_running_func():
    user_obj = User(
        first_name='suljsdfsdo3',
        last_name='suljewssqfddsfc',
        username='sufqswsdqqqf3',
        email='sucqqqsfd3qqq3@gmail.com',
        is_active=True,
    )
    user_obj.set_password('pavle')
    user_obj.save()


class Worker2TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        long_running_func.delay()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        "gossip", {"type": "user.gossip",
                   "event": "New Post trololo",
                   "username": 'pavle'})

        return JsonResponse({'foolo': 'barlo'})
