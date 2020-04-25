from rq.job import Job

from main.models import Post, Comment, UserFollowing, User
from django.db.models import Q
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)

from .pagination import (
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
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .permissions import IsOwnerOrReadOnly

from .serializers import (
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    PostListSerializer,
)

from django_rq import job
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @job
# def long_running(text):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "post", {"type": "post.notif",
#                    "event": "This user has created a new post",
#                    "username": "text"})
#     pass


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['text', 'user__username']
    pagination_class = PostPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # followed_people = UserFollowing.objects.filter(user_id=self.request.user.id).values('following_user_id')
        # print(followed_people)

        queryset_list=Post.objects.filter(
            is_public=False,
            user__following__follower=self.request.user.id,
            is_approved=True
        ) | Post.objects.filter(is_public=True).exclude(user=self.request.user.id)
        
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(text__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list

# Create your views here.
# @api_view(['POST',])
# def registration_view(request):
#     if request.method == 'POST':
#         serializer = RegiuserstrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'successfully registered a new user'
#             data['email'] = user.email
#             data['username'] = user.username
#         else:
#             data = serializer.errors
#         return Response(data)
#
# class UserView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
# class PostView(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class CommentView(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#
# class UserFollowingView(viewsets.ModelViewSet):
#     queryset = UserFollowing.objects.all()
#     serializer_class = UserFollowingSeliazer
