from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("category", views.Category, name="category"),
    path("listing/<int:id>/", views.listing, name="listing"),
    path("yourAuction/", views.yourAuction, name="yourAuction"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)