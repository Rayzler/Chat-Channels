from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.frontpage, name="frontpage"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout")
]
