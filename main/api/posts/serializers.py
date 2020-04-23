from django.core.validators import RegexValidator
from django.contrib.auth import password_validation, authenticate
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from rest_framework.fields import CharField, BooleanField

from main.models import Post, Comment, UserFollowing
from main.api.comments.serializers import CommentSerializer
from main.api.users.serializers import UserDetailSerializer


class PostCreateUpdateSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'text',
            'user',
            'is_approved'
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
            'is_approved',
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
    following = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'text',
            'user',
            'is_approved',
            'following',
        ]

    def get_following(self, obj):
        return UserFollowing.objects.filter(following=obj.user).exists()

# class UserSerializer(ModelSerializer):
#     name_regex = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
#     first_name = serializers.CharField(max_length=60, required=True, validators=[name_regex])
#     last_name = serializers.CharField(max_length=60, required=True, validators=[name_regex])
#     email = serializers.EmailField(max_length=30, required=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name', 'username', 'email')
#
#
# class RegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
#     name_regex = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
#     first_name = serializers.CharField(max_length=60, required=True, validators=[name_regex])
#     last_name = serializers.CharField(max_length=60, required=True, validators=[name_regex])
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#     def save(self):
#         user = User(
#             first_name = self.validated_data['first_name'],
#             last_name = self.validated_data['last_name'],
#             username = self.validated_data['username'],
#             email = self.validated_data['email'],
#         )
#
#         password = self.validated_data['password']
#         password2 = self.validated_data['password2']
#         # if self.validated_data['password'] != self.validated_data['password2']:
#         #     raise serializers.ValidationError({'password': 'muu ne poklapa seee'})
#         if password != password2:
#             raise serializers.ValidationError({'password': 'Passwords must match.'})
#         user.set_password(password)
#         user.save()
#         return user
#
# class LoginSerializer(serializers.ModelSerializer):
#     token = CharField(allow_blank=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'token']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }
#
#
#
# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('id', 'text', 'user', 'is_public', 'is_approved')
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('id', 'user_id', 'post_id', 'text', 'is_approved')
#
#
# class UserFollowingSeliazer(serializers.ModelSerializer):
#     class Meta:
#         model = UserFollowing
#         fields = ('user_id', 'following_user_id')
