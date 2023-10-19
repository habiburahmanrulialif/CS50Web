from django.shortcuts import render
import random
from . import util

import markdown2

def all_upper(my_list):
            return [x.upper() for x in my_list]

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/404.html") 
    text = markdown2.Markdown()
    return render(request, "encyclopedia/entry-page.html", {
        "title": title,
        "content": text.convert(util.get_entry(title))
    })


def new_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    return render(request, "encyclopedia/new-page.html")


def edit_page(request, title):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit-page.html",{
        "content": content,
        "title": title
    })


def search(request):
    querry = request.GET.get('q')
    querry = querry.upper()
    if util.get_entry(querry) is None:
        entries = util.list_entries()
        entries = all_upper(entries)
        entry = [i for i in entries if querry in i]
        if entry:
            return render(request, "encyclopedia/index.html", {
                "entries": entry
            })
        
        '''
        Should return 404 page
        '''
        return render(request, "encyclopedia/404.html")
    
    
    text = markdown2.Markdown()
    return render(request, "encyclopedia/entry-page.html", {
        "title": querry,
        "entries": text.convert(util.get_entry(querry))
    })


def random_page(request):
    title = util.list_entries()
    title = random.choice(title)
    text = markdown2.Markdown()
    return render(request, "encyclopedia/entry-page.html", {
        "title": title,
        "content": text.convert(util.get_entry(title))
    })