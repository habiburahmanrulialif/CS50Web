from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("category", views.Category, name="category"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("unlist/<int:id>/", views.unlist, name="unlist"),
    path("yourAuction/", views.yourAuction, name="yourAuction"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wish/<int:id>/", views.wish, name="wish"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]