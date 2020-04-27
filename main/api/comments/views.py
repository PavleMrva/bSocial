from django.db.models import Q
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
    CommentSerializer,
    CommentCreateUpdateSerializer,
)

from main.models import Comment


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(text__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list
