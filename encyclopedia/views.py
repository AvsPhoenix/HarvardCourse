import random
from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from markdown2 import Markdown

from . import util


def index(request):

    if(request.method == "POST"):

        search = request.POST["q"]
        result = util.get_entry(search)

        if(result == None):

            listElems = util.list_entries()
            listResults = []
            for elem in listElems:
                if(search.lower() in elem.lower()):
                    listResults.append(elem)

            if(listResults == []):

                return render(request, "encyclopedia/error.html", {
                    "title": "No results found",
                    "error": "The term searched has not results."
                })
            
            else:

                return render(request, "encyclopedia/index.html", {
                    "entries": listResults,
                    "title": "Wiki Encyclopedia"
                })                

        else:
            return GetItem(request, search)
    
    else:

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "title": "Wiki Encyclopedia",
            "item_selected" : False
        })

def GetItem(request, name):

    if(util.get_entry(name) == None):

        return render(request, "encyclopedia/error.html", {
            "title": "Page not found",
            "error": "There are not data found."
        })
    
    else:

        markdowner = Markdown()
        definition = util.get_entry(name)

        return render(request, "encyclopedia/index.html", {
            "definition": markdowner.convert(definition),
            "title": name,
            "item_selected" : True
        })


class NewWikiItemForm(forms.Form):
    
    title = forms.CharField(label="Type title", max_length=20, required=True)
    info = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'columns': 5, 'name': 'txtInfo'}), required=True)


def edit(request, item):

    form = NewWikiItemForm()
    result = util.get_entry(item)

    if(result != None):

        form.fields["title"].initial = item
        form.fields["info"].initial = result
    
        return render(request, "encyclopedia/add.html", {
            "form": form,
            "title": "Edit Item"
        })
    
def randomPage(request):

    listElems = util.list_entries()

    if(len(listElems) > 0):
        randNumber = random.randint(1, len(listElems)) - 1
        return GetItem(request, listElems[randNumber])

    else:
        return render(request, "encyclopedia/error.html", {
            "title": "No data",
            "error": "There are no data in database."            
        })
    


def add(request):

    if(request.method == "POST"):

        form = NewWikiItemForm(request.POST)

        if(not form.is_valid()):

            return render(request, "encyclopedia/error.html", {
                "title": "Error in data",
                "error": "The data is wrong or empty."
            })
        
        title = form.cleaned_data["title"]
        title = title.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

        info = form.cleaned_data["info"]
        info = info.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                
        '''
        if(util.get_entry(title) == None):                
            util.save_entry(title, info)
        else:
            return render(request, "encyclopedia/error.html", {
                "title": "Page already exits",
                "error": "The information already exists."
            })
        '''
        
        return render(request, "encyclopedia/add.html", {
            "form": NewWikiItemForm(),
            "title": "Wiki Encyclopedia"
        })        

    else:

        form = NewWikiItemForm()
    
        return render(request, "encyclopedia/add.html", {
            "form": form,
            "title": "Wiki Encyclopedia: "
        })
