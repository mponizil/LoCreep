from locreep.models import *

from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
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
    return render_to_response("welcome.html", { 'header': 'large' })

@csrf_exempt
def register(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    u = User.objects.create_user(email,email,password)
    u.first_name = fname
    u.last_name = lname
    u.save()
    
    #login(request, u)
    
    return HttpResponse('{ "success": true }')

def login(request):
    return render_to_response("login.html")

@csrf_exempt
def auth(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    
    user = authenticate(username=email,password=password)
    
    if user is not None:
        login(request, user)
        return HttpResponse('{ "success": true }')
    else:
        return HttpResponse('{ "success": false, "error": "The email and password you entered were not found." }')

@csrf_exempt
@require_POST
def tumblr_text(request):
    conversation_id = request.POST.get('conversation_id')
    title = request.POST.get('title')
    body = request.POST.get('body')
    
    tumblr = Api(BLOG,USER,PASSWORD)
    post = tumblr.write_regular(title, body)

    return HttpResponse(title + "\n" + body)