from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path("add", views.add, name="add"),    
    path("wiki/edit/<str:item>", views.edit, name="edit"),    
    path("randomPage", views.randomPage, name="randomPage"),    
    path("", views.index, name="index"),
    path("<str:name>", views.GetItem, name="item")
        
    
]
