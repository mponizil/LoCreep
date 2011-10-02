from locreep import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from twilio.rest import TwilioRestClient

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
client = TwilioRestClient(account, token)

def welcome(request):
    return HttpResponse("wassup")

def phone(request):
    return HttpResponse("phone")

def text(request):
    print('yay')
    #print str(request.POST)
    # message = client.sms.messages.create(to="+17608463179",
    #                                      from_="+13475148471",
    #                                      body="Hello!")
    return HttpResponse('success')

def my_groups(request):
    return render_to_response("my-groups.html")

def create(request):
    return render_to_response("create.html")