from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.contrib.auth import password_validation, authenticate
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    CharField,
    EmailField,
)
from rest_framework.fields import CharField

from main.models import User, UserFollowing
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class UserCreateSerializer(ModelSerializer):
    name_regex = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
    first_name = CharField(max_length=30, required=True, validators=[name_regex])
    last_name = CharField(max_length=30, required=True, validators=[name_regex])
    email = EmailField(max_length=30, required=True)
    password = CharField(min_length=8, required=True, error_messages={'min_length': 'Ensure that the password field has at least 8 characters'})
    password2 = CharField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]
        extra_kwargs = {"password":
                            {"write_only": True,},
                        "password2":
                            {"write_only": True},
                        }
        
    
    def validate(self, data):    
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("The user with this email is already registered")
        return data
    
    def validate_password(self, value):
        data = self.get_initial()
        pass1 = data.get('password2')
        pass2 = value
        if pass1 != pass2:
            raise ValidationError('Passwords must match')
        return value
        
    def validate_password2(self, value):
        data = self.get_initial()
        pass1 = data.get('password')
        pass2 = value
        if pass1 != pass2:
            raise ValidationError('Passwords must match')
        return value
    
    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        user_obj = User(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            is_active = False,
        )
        user_obj.set_password(password)
        user_obj.save()
        current_site = get_current_site(self.context['request'])
        email_subject = "Activate your account"
        message = render_to_string('register/activate.html',
                                   {
                                       'user': user_obj,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                                       'token': account_activation_token.make_token(user_obj),
                                   })

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email_message.send()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(required=False, allow_blank=True)
    password = CharField(min_length=8, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True},
                        }
        
    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data['password']
        if not email or not username:
            raise ValidationError("A username or email is required to login")
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")
        
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials. Please try again.')
            
        data["token"] = "SOME RANDOM TOKEN"
        return data
