from django.urls import path
from . import views

app_name = "wiki"

urlpatterns = [
    path("add", views.add, name="add"),
    path("", views.index, name="index"),
    path("<str:name>", views.GetItem, name="item")
    # path("", views.search, name="search")
]
