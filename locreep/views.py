from locreep import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

def welcome(request):
    return HttpResponse("wassup")