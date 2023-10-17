from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_page", views.add_page, name="add_page"),
    path("<str:entry>", views.entry, name="entry")
]
