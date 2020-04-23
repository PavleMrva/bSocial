from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation, authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.fields import CharField

from main.models import Comment
from main.api.users.serializers import UserDetailSerializer


class CommentCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'text',
            'post',
            'user',
            'is_approved'
        ]

class CommentSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'text',
            'user',
            'is_approved'
        ]

