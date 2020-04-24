from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from djoser.conf import User

from main.api.users.tokens import account_activation_token
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def register(response):
    return render(response, "register/registration.html")

def login(response):
    return render(response, "register/login.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as id:
            user=None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
        return render(request,'auth/activate_failed.html', status=401)

