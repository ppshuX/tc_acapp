from django.shortcuts import render


def index(request):
    return render(request, "myspace/index.html")

