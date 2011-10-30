from locreep.models import *

from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
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

def welcome_pg(request):
    if not request.user.is_authenticated():
        return render_to_response("welcome.html", { 'header': 'large' }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/dashboard')

@csrf_exempt
@require_POST
def register(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    
    u = User.objects.create_user(email,email,password)
    u.first_name = fname
    u.last_name = lname
    u.save()
    
    user = authenticate(username=email,password=password)
    login(request, user)
    
    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def update_user(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    
    if request.user.is_anonymous():
        u = User.objects.get(username=email)
    else:
        u = request.user
        
    u.first_name = fname
    u.last_name = lname
    u.username = email
    u.set_password(password)
    u.save()

    user = authenticate(username=email,password=password)
    login(request, user)

    return HttpResponse('{ "success": true }')

def login_pg(request):
    return render_to_response("login.html", context_instance=RequestContext(request))

@csrf_exempt
@require_POST
def auth(request):
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(username=email,password=password)
    
    if user is not None:
        login(request, user)
        return HttpResponse('{ "success": true }')
    else:
        return HttpResponse('{ "success": false, "error": "The email and password you entered were not found." }')

def logout_pg(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
@require_POST
def tumblr_text(request):
    conversation_id = request.POST['conversation_id']
    title = request.POST['title']
    body = request.POST['body']
    
    tumblr = Api(BLOG,USER,PASSWORD)
    post = tumblr.write_regular(title, body)

    return HttpResponse(title + "\n" + body)