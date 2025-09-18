from django.urls import path, re_path
from game.views.kof.index import index

urlpatterns = [
    path("", index, name="kof_index"),
]
