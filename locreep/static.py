from locreep.models import *

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def video(request):
    return render_to_response("video.html", context_instance=RequestContext(request))

def how_to(request):
    return render_to_response("how-to.html", context_instance=RequestContext(request))

def terms(request):
    return render_to_response("terms.html", context_instance=RequestContext(request))

def contact(request):
    return render_to_response("contact.html", context_instance=RequestContext(request))

def press(request):
    return render_to_response("press.html", context_instance=RequestContext(request))