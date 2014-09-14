from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    if 'user_id' in request.session and request.session['user_id']:
        return redirect(reverse('connect_apps'))
    else:
        return render(request, "index.html", {})


def close_window(request):
    return HttpResponse("<script>window.open('', '_self', '');window.close();</script>")