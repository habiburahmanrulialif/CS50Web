from django.shortcuts import render

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if util.get_entry(entry) is None:
        return render(request, "encyclopedia/entry-page.html", {
        "title": entry,
    })    
    text = markdown2.Markdown()
    return render(request, "encyclopedia/entry-page.html", {
        "title": entry,
        "entries": text.convert(util.get_entry(entry))
    })


def new_page(request):
    return render(request, "encyclopedia/new-page.html")


def search(request):
    find = entry(request)