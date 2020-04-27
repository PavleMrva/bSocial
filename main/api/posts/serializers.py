from django.core.validators import RegexValidator
from django.contrib.auth import password_validation, authenticate
from django.db.models import DateTimeField
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.fields import CharField, BooleanField, DateTimeField

from main.models import Post, Comment, UserFollowing
from main.api.comments.serializers import CommentSerializer
from main.api.users.serializers import UserDetailSerializer
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer



class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'text',
            'is_public'
        ]

class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'text',
            'user',
            'comments',
        ]

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='post-api:detail',
    )

    user = UserDetailSerializer(read_only=True)
    created_at = DateTimeField(format="%d/%m/%Y at %H:%M:%S", input_formats=None, default_timezone=None)
    following = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'text',
            'user',
            'created_at',
            'following',
        ]
        ordering = ['created_at']

    def get_following(self, obj):
        return UserFollowing.objects.filter(follower=self.context['request'].user, following=obj.user).exists()

# class PostDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = PostDocument
#         fields = [
#             'url',
#             'id',
#             'text',
#             'user',
#             'created_at',
#             'following',
#         ]