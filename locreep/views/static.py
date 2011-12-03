from locreep.models import *

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def video(request):
    return render(request, "video.html")

def how_to(request):
    return render(request, "how-to.html")

def terms(request):
    return render(request, "terms.html")

def contact(request):
    return render(request, "contact.html")

def press(request):
    return render(request, "press.html")