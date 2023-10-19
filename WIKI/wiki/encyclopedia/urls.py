from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_page", views.new_page, name="add_page"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.entry, name="entry")
]
