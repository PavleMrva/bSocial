from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def register(response):
    return render(response, "register/registration.html")

def login(response):
    return render(response, "register/login.html")
