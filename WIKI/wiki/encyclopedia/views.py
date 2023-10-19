from django.shortcuts import render

from . import util

import markdown2

def all_upper(my_list):
            return [x.upper() for x in my_list]

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