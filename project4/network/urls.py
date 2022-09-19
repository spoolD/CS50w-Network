
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like", views.like, name="like"),
    path("post", views.post, name="post"),
    path("follow", views.follow, name="follow"),
    path("following", views.index, name="following"),
    path("profile/<str:author>", views.profile, name="profile")
]
