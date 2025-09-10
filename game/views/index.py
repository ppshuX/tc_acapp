from django.shortcuts import render


def index(request):
    return render(request, "multiends/web.html") #路由从templates后面开始写
