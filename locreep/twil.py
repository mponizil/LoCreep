from locreep.models import *

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from twilio.rest import TwilioRestClient
from twilio import twiml

from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST

import urllib
import urllib2

domain_name = "http://locreep.com"

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
tc = TwilioRestClient(account, token)

@csrf_exempt
@require_POST
def text(request):
    creep_phone = request.POST['From']
    group_phone = request.POST['To']
    body = request.POST['Body']
    
    # creep_phone = '+17608463179'
    # group_phone = '+13475148471'
    # body = 'sup'
    
    # find the group
    try:
        group = Group.objects.get(phone=group_phone)
    except Group.DoesNotExist:
        return HttpResponse('no group with this phone number')
    
    # check if it's from a creep we know
    try:
        creep = Creep.objects.get(phone=creep_phone)
    except Creep.DoesNotExist:
        creep = Creep(phone=creep_phone)
        creep.save()
    
    try:
        group = Group.objects.get(phone=group_phone,creeps=creep)
    except Group.DoesNotExist:
        group.creeps.add(creep)
    
    # check if conversation with this creep is going on
    try:
        conversation = Conversation.objects.get(group=group,creep=creep)
    except Conversation.DoesNotExist:
        conversation = Conversation(group=group,creep=creep)
        conversation.save()
    
    # create message
    message = Message(conversation=conversation,user_type='creep',creep=creep,body=body)
    message.save()
    
    # broadcast to chat room
    url = 'http://locreep.com:3000/message'
    values = {
        'group_id' : group.id,
        'conversation_id' : conversation.id,
        'user_type' : 'creep',
        'creep_phone' : creep.phone,
        'message' : body
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    # send reply
    # sms = tc.sms.messages.create(to = creep_phone, from_ = group_phone, body = "lol you're funny!")
    
    return HttpResponse('{ "success": true }')

@csrf_exempt
def save_creepy_voice(request):
    group_phone = request.GET['To']
    creep_phone = request.GET['From']
    body = request.GET['RecordingUrl'] + '.mp3'
    
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
        conversation = Conversation.objects.get(group=group,creep=creep)
    except Conversation.DoesNotExist:
        conversation = Conversation(group=group,creep=creep)
        conversation.save()
    
    message = Message(conversation=conversation,user_type='creep',creep=creep,body=body)
    message.save()
    
    # broadcast to chat room
    url = 'http://locreep.com:3000/message'
    values = {
        'group_id' : group.id,
        'conversation_id' : conversation.id,
        'user_type' : 'creep',
        'creep_phone' : creep.phone,
        'message' : body
    }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    
    return HttpResponse('{ "success": true }')

@csrf_exempt
def phone(request):	
    r = twiml.Response()
    r.say("hello")
    r.record(action=domain_name+"/save_creepy_voice", method="GET")
    return HttpResponse(str(r))