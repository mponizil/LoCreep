from locreep import models
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from twilio.rest import TwilioRestClient
import logging
logger = logging.getLogger() 
handler = logging.FileHandler("/opt/bitnami/apps/django/django_projects/test_site/test.log")
logger.addHandler(handler)

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
client = TwilioRestClient(account, token)

def welcome(request):
    return HttpResponse("wassuzzp")

def phone(request):
    return HttpResponse("phone")

def text(request):
    print('yay')
    #print str(request.POST)
    # message = client.sms.messages.create(to="+17608463179",
    #                                      from_="+13475148471",
    #                                      body="Hello!")
    logger.debug(request.POST) 
    logger.debug("THIS IS A TEST")
    return HttpResponse(request.POST)

def create(request):
    return render_to_response("create.html")

def myGroups(request):
    context={}
    return render_to_response('myGroups.html', context, context_instance=RequestContext(request))
