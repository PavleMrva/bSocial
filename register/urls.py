from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('activate/<uidb64>/<token>/',views.ActivateAccountView.as_view(), name='activate'),
]
