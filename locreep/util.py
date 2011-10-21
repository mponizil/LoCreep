from locreep.models import *

from django.template import RequestContext, loader
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST
from tumblr import Api

BLOG = "locreep.tumblr.com"
USER = "locreep@mailinator.com"
PASSWORD = "locreep"

def welcome(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/group/1")
    else:
        return render_to_response("welcome.html", { 'header': 'large' })

def login(request):
    return render_to_response("login.html")

@csrf_exempt
@require_POST
def tumblr_text(request):
    conversation_id = request.POST.get('conversation_id')
    title = request.POST.get('title')
    body = request.POST.get('body')
    
    tumblr = Api(BLOG,USER,PASSWORD)
    post = tumblr.write_regular(title, body)

    return HttpResponse(title + "\n" + body)