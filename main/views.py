from django.shortcuts import render

def home(response):
    return render(response, "main/home.html")

def post(response):
    return render(response, "main/post.html")


