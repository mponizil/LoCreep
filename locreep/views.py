from locreep import models
from models import *
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from twilio.rest import TwilioRestClient
from twilio import twiml
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
client = TwilioRestClient(account, token)

def welcome(request):
    return HttpResponse("wassup")

@csrf_exempt
@require_POST
def text(request):
    creep_phone = request.POST.get('From')
    group_phone = request.POST.get('To')
    body = request.POST.get('Body')

    # check if it's from a creep we know
    try:
        creep = Creep.objects.get(phone=creep_phone)
    except Creep.DoesNotExist:
        creep = Creep(phone=creep_phone)
        creep.save()
    
    # find the group
    try:
        group = Group.objects.get(phone=group_phone)
    except Group.DoesNotExist:
        return HttpResponse('no group with this phone number')
    
    # check if conversation with this creep is going on
    try:
        conversation = Conversation.objects.get(group=group)
    except Conversation.DoesNotExist:
        conversation = Conversation(group=group,creep=creep)
        conversation.save()
    
    # create message
    message = Message(conversation=conversation,user_type='creep',creep=creep,body=body)
    message.save()
    
    sms = client.sms.messages.create(to = creep_phone, from_ = group_phone, body = "lol you're funny!")
    
    return HttpResponse('success')

def create(request):
    return render_to_response("create.html")

def creep(request, creep_id):
    creep = Creep.objects.filter(id=creep_id)
    return render_to_response("creep.html",{'creep':creep})

def confirmInvite(request, user_id):
    user = User.objects.filter(id=user_id)
    return render_to_response("confirmInvite.html",{'user':user})

def twilio(request):
    # print 'here'
    # print request
    # message = client.sms.messages.create(to="+17608463179",
    #                                      from_="+13475148471",
    #                                      body="Hello!"
    return HttpResponse(str(request.POST)+"hello")

@csrf_exempt
def call(request):
    return HttpResponse(request)
    
def xml(request):
    r = twiml.Response()
    r.say("hello")
    r.record(action="http://locreep.com/test_site/call/")
    return HttpResponse(str(r))

def myGroups(request):
	
    # call = client.calls.create(to="+19178551541", from_="+13475148471", url="http://foo.com/call.xml")
    # print call.length
    # print call.sid
	
    call = client.calls.create(to="9178551541", from_="3475148471", url="http://locreep.com/test_site/xml/")
	
    # sid = call.sid
    # call = client.calls.get(sid)
	
    # print call.notifications.list()
    # print call.recordsings.list()
    # print call.transcriptions.list()
    return HttpResponse(request)
