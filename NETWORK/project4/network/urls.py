from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profiles/<int:id>", views.profiles, name="profiles"),
    path("following/", views.FollowingPostFront, name="following"),
    

    #API
    path("post/", views.PostApi, name="post"),
    path("posting/", views.posting, name="posting"),
    path("post/<int:postId>", views.PostDetailAPI, name="post_detail"),
    path("profile/<int:id>/", views.profile, name="profile"),
    path("postEdit/<int:id>", views.editPost, name="post_edit"),
    path("account/<int:id>", views.FollowApi, name="account_detail"),
    path('check_like_status/<int:post_id>/', views.check_like_status, name='check_like_status'),

    #For Following and UnFollowing
    path("follow/<int:id>", views.Following, name="follow"),
    #Post for 
    path("followpost/", views.FollowingPost, name="follow_post"),
]
