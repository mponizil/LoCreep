from locreep.models import *

from django.template import RequestContext, loader
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from twilio.rest import TwilioRestClient
from twilio import twiml

from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

import urllib
import urllib2
import json

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
tc = TwilioRestClient(account, token)

def dashboard(request):
    try:
        groups = Group.objects.filter(users=request.user)
    except Group.DoesNotExist:
        groups = None
    
    return render_to_response("dashboard.html", { 'groups': groups })

def group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return HttpResponse("no group found")
    
    conversations = Conversation.objects.filter(group=group)
    
    return render_to_response("group.html", { 'conversations': conversations })
    
def conversation(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return HttpResponse("no conversation found")
    
    messages = Message.objects.filter(conversation=conversation).order_by('-id')
    
    longUrl = urllib.quote_plus('http://locreep.com/conversation/' + str(conversation.id))
    f = urllib2.urlopen('http://api.bitly.com/v3/shorten?login=afcampa&apiKey=R_a2e5411ee02dc84186802a509dfb4ced&longUrl='+longUrl+'%2F&format=json')
    a = json.loads(f.read())
    qr = a['data']['url']+'.qrcode'
    
    return render_to_response("conversation.html", { 'conversation_id': conversation.id, 'creep': conversation.creep, 'messages': messages, 'qr': qr })

@csrf_exempt
def user_message(request):
    conversation_id = request.POST.get('conversation_id')
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return HttpResponse('no conversation')

    user = request.user
    body = request.POST.get('body')

    message = Message(conversation=conversation,user_type='user',body=body)
    message.save()

    url = 'http://localhost:3000/message/'
    values = {'conversation_id' : conversation_id,
              'user_type' : 'user',
              'message' : body }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print tc

    sms = tc.sms.messages.create(to = conversation.creep.phone, from_ = conversation.group.phone, body = body)

    return HttpResponse('{success:true}')