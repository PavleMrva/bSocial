from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from rest_framework import status
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
    UserFollowsSerializer,
)

from main.models import User, UserFollowing

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


class UserFollowingAPIView(CreateAPIView):
    def post(self, request, format=None):
        user = request.user
        follow = User.objects.get(username=self.request.data.get('following'))
        user_following = UserFollowing(following=follow, follower=user)
        try:
            user_following.save()
            return JsonResponse(
                {'status': status.HTTP_200_OK, 'data': "following", 'message': "follow" + str(follow.id)})
        except:
            UserFollowing.objects.get(following=follow, follower=user).delete()
            return JsonResponse({'status': status.HTTP_200_OK, 'data': "unfollowing", 'message': "follow" + str(follow.id)})


