from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True)

    name_regex = RegexValidator(r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    first_name = forms.CharField(max_length=60, required=True, validators=[name_regex])
    last_name = forms.CharField(max_length=60, required=True, validators=[name_regex])

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        help_texts = {
            'username': None,
            'email': None,
        }

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ["username", "password1"]