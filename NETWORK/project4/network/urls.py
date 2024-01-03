from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API
    path("post/", views.PostApi, name="post"),
    path("posting/", views.posting, name="posting"),
    path("post/<int:postId>", views.PostDetailAPI, name="post_detail"),
    path("account/<>int:id", views.FollowApi, name="account_detail"),
]
