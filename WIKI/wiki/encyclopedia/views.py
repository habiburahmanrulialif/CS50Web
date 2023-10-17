from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    return render(request, "encyclopedia/entry-page.html", {
        "title": entry
    })


def add_page(request):
    return render(request, "encyclopedia/add-page.html")