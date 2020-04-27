from django.contrib.auth.models import User
from django.shortcuts import render

from main.models import Post


def home(response):
    return render(response, "main/home.html")


def post_detail(response, pk):
    post = Post.objects.get(pk=pk)
    user = post.user
    args = {'post': post, 'user': user}
    return render(response, "main/post.html", args)
