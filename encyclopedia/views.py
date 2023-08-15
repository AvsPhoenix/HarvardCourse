from django import forms
from django.http import HttpResponse
from django.shortcuts import render

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
                    "subject": "No results found",
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
            "title": "Wiki Encyclopedia"
        })

def GetItem(request, name):

    if(util.get_entry(name) == None):

        return render(request, "encyclopedia/error.html", {
            "subject": "Page not found",
            "error": "There are not data found."
        })
    
    else:

        return render(request, "encyclopedia/index.html", {
            "definition": util.get_entry(name),
            "title": name
        })


class NewWikiItemForm(forms.Form):
    subject = forms.CharField(label="Type subject", max_length=20, required=True)
    
    # info = forms.CharField(label="Information", widget=forms.Textarea(attrs={"rows": 2, "columns": 2, "placeholder":"Type information", "id": "txtAreaInformation"}), required=True)
    info = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'columns': 5, 'name': 'txtInfo'}))


def add(request):

    if(request.method == "POST"):

        subject = request.POST["subject"]
        info = request.POST["info"]        

    else:
    
        return render(request, "encyclopedia/add.html", {
            "form": NewWikiItemForm(),
            "title": "Wiki Encyclopedia"
        })


'''
def search(request):


    return render(request, "encyclopedia/index.html", {
        "definition": util.get_entry("HTML"),
        "title": "HTML"
    })

    if(request.method == "POST"):
        formulario = request.POST
        search = formulario.q

        

        #return item(request, search)

'''