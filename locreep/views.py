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
import urllib
import urllib2

domain_name = "http://3bbq.localtunnel.com"

# from django.views.decorators.http import require_POST


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
    
    # broadcast to chat room
    url = 'http://localhost:3000/message'
    values = {'conversation_id' : conversation.id,
              'user_type' : 'creep',
              'message' : body }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    # send reply
    sms = client.sms.messages.create(to = creep_phone, from_ = group_phone, body = "lol you're funny!")
    
    return HttpResponse('{success:true}')

def create(request):
    return render_to_response("create.html")

def creep(request, creep_id):
    creep = Creep.objects.filter(id=creep_id)
    return render_to_response("creep.html",{'creep':creep})

def confirmInvite(request, user_id):
    user = User.objects.filter(id=user_id)
    return render_to_response("confirmInvite.html",{'user':user})

def save_creepy_voice(request):
    To = request.GET.get('To','')
    From = request.GET.get('From','')
    Body = request.GET.get('RecordingUrl','')+'.mp3'
    print To
    print From
    print Body
    group = Group.objects.get(phone=To)
    creep = Creep.objects.get(phone=From)
    conversation = Conversation.objects.get(group=group,creep=creep)
    message = Message(conversation=conversation,user_type='creep',creep=creep,body=Body)
    message.save()
    return HttpResponse("ends.")

@csrf_exempt
def phone(request):	
    r = twiml.Response()
    r.say("hello")
    r.record(action=domain_name+"/save_creepy_voice/", method="GET")
    return HttpResponse(str(r))

@csrf_exempt
def user_message(request):
    conversation_id = request.POST.get('conversation_id')
    conversation = Conversation.objects.get(id=conversation_id)
    user = request.user
    body = request.POST.get('body')
    
    message = Message(conversation=conversation,user_type='user',user=user,body=body)
    message.save()

    url = 'http://localhost:3000/message'
    values = {'conversation_id' : conversation_id,
              'user_type' : 'user',
              'message' : body }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    return HttpResponse('{success:true}')

def chat(request):
    return render_to_response("chat.html")