from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "index.html", {})


def close_window(request):
    return HttpResponse("<script>window.open('', '_self', '');window.close();</script>")