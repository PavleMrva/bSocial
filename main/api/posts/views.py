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
    AllowAny)

from .permissions import IsOwnerOrReadOnly

from .serializers import (
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    PostListSerializer,
)

# from django_elasticsearch_dsl_drf.constants import (
#     LOOKUP_FILTER_RANGE,
#     LOOKUP_QUERY_GT,
#     LOOKUP_QUERY_GTE,
#     LOOKUP_QUERY_IN,
#     LOOKUP_QUERY_LT,
#     LOOKUP_QUERY_LTE,
#     SUGGESTER_COMPLETION,
# )
# from django_elasticsearch_dsl_drf.filter_backends import (
#     DefaultOrderingFilterBackend,
#     FacetedSearchFilterBackend,
#     FilteringFilterBackend,
#     SearchFilterBackend,
#     SuggesterFilterBackend,
# )
# from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
#
# from search.documents import PostDocument
# from .serializers import PostDocumentSerializer

# class PostViewSet(DocumentViewSet):
#     document = PostDocument
#     serializer_class = PostDocumentSerializer
#     permission_classes = [AllowAny]
#     ordering = ('created_at',)
#     lookup_field = 'id'
#
#     filter_backends = [
#         DefaultOrderingFilterBackend,
#         # FacetedSearchFilterBackend,
#         # FilteringFilterBackend,
#         # SearchFilterBackend,
#         # SuggesterFilterBackend,
#     ]
#
#     search_fields = (
#         'text',
#     )
#
#     # filter_fields = {
#     #     'id': {
#     #         'field': 'id',
#     #         'lookups': [
#     #             LOOKUP_FILTER_RANGE,
#     #             LOOKUP_QUERY_IN,
#     #             LOOKUP_QUERY_GT,
#     #             LOOKUP_QUERY_GTE,
#     #             LOOKUP_QUERY_LT,
#     #             LOOKUP_QUERY_LTE,
#     #         ],
#     #     },
#     # }
#
#     # suggester_fields = {
#     #     'name_suggest': {
#     #         'field': 'name.suggest',
#     #         'suggesters': [
#     #             SUGGESTER_COMPLETION,
#     #         ],
#     #     },
#     # }

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
    pagination_class = PostLimitOffsetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        # followed_people = UserFollowing.objects.filter(user_id=self.request.user.id).values('following_user_id')
        # print(followed_people)

        queryset_list=Post.objects.filter(
            is_public=False,
            user__following__follower=self.request.user.id,
        ) | Post.objects.filter(is_public=True).exclude(user=self.request.user.id)
        
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(text__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list

