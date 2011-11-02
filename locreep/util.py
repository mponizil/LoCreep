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

import os, re, sys, random, string

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
    
    if not fname or not lname or not email or not password:
        return HttpResponse('{ "success": false, "error": "Please enter all the fields." }')
        
    if User.objects.filter(username=email).count() > 0:
        return HttpResponse('{ "success": false, "error": "The email you entered already exists." }')
    
    user = User.objects.create_user(email,email,password)
    user.first_name = fname
    user.last_name = lname
    user.save()
    
    auth_user = authenticate(username=email,password=password)
    login(request, auth_user)
    
    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def update_user(request):
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    
    if request.user.is_anonymous():
        user = User.objects.get(username=email)
    else:
        user = request.user
        
    user.first_name = fname
    user.last_name = lname
    user.username = email
    user.set_password(password)
    user.save()

    auth_user = authenticate(username=email,password=password)
    login(request, auth_user)

    return HttpResponse('{ "success": true }')

def login_pg(request):
    return render_to_response("login.html", { 'header': 'large' }, context_instance=RequestContext(request))

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
    
    # create a dictionary mapping names to random strings so they are unrecognizable but consistent
    replacements = generate_replacements()

    # strip credit card numbers
    credit_pattern = re.compile(r"\d{3,5}\D*\d{3,5}\D*\d{3,5}\D*\d{3,5}")
    body = credit_pattern.sub("XXXX-XXXX-XXXX-XXXX", body)

    # strip phone numbers
    phone_pattern = re.compile(r"(\d{3}\D*)?(\d{3})\D*(\d{4})")
    body = phone_pattern.sub("XXX-XXXX", body)

    # strip names
    #TODO: make sure names.txt is in correct directory relative to server
    names_path = os.path.dirname(__file__) + '/../names.txt'
    names = open(names_path, 'r')
    for name in names:
        name = name.rstrip() # remove newline
        name_pattern = re.compile(r"\b" + name + r"\b", re.IGNORECASE)
        body = name_pattern.sub(replacements[name], body)

    tumblr = Api(BLOG,USER,PASSWORD)
    post = tumblr.write_regular(title, body)

    return HttpResponse(title + "\n" + body)

def generate_replacements():
    names_path = os.path.dirname(__file__) + '/../names.txt'
    names = open(names_path, 'r')
    replacements = {}
    for name in names:
        name = name.rstrip()
        replacements[name] = ''.join(random.choice(string.ascii_uppercase) for x in range(len(name)))
    return replacements

def how_to(request):
    return render_to_response("how-to.html", context_instance=RequestContext(request))

def terms(request):
    return render_to_response("terms.html", context_instance=RequestContext(request))

def contact(request):
    return render_to_response("contact.html", context_instance=RequestContext(request))