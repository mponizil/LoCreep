from locreep import models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from twilio.rest import TwilioRestClient
from twilio import twiml
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST

# from django.views.decorators.http import require_POST


account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
client = TwilioRestClient(account, token)

def welcome(request):
    return HttpResponse("wassup")

def phone(request):
    return HttpResponse("phone")

def twilio(request):
    # print 'here'
    # print request
    # message = client.sms.messages.create(to="+17608463179",
    #                                      from_="+13475148471",
    #                                      body="Hello!"
    return HttpResponse(str(request.POST)+"hello")

# @require_POST
def call(request):
    To = request.GET.get('To','')
	From = request.GET.get('From','')
	Body = request.GET.get('RecordingUrl','')+'.mp3'
	group = Group.objects.get(phone=To)
	creep = Creep.objects.get(phone=From)
	conversation = Conversation.objects.get(group=group,creep=creep)
	message = Message(conversation=conversation,user_type='creep',creep=creep,body=Body)
	message.save()
	return HttpResponse("ends.")
    # print str(request.POST)+"hello"
    # print str(request.GET)+"hellohello"
    # return HttpResponse(str(request.POST)+"hello")

	



@csrf_exempt
def phone(request):	
    r = twiml.Response()
    r.say("hello")
    r.record(action="http://3bbq.localtunnel.com/call/", method="GET")
    return HttpResponse(str(r))
	
@csrf_exempt
   
def xml(request):
	
    r = twiml.Response()
    r.say("hello")
    r.record(action="http://3bbq.localtunnel.com/call/", method="GET")
    return HttpResponse(str(r))

def myGroups(request):
	
    # call = client.calls.create(to="+19178551541", from_="+13475148471", url="http://foo.com/call.xml")
    # print call.length
    # print call.sid
	
    call = client.calls.create(to="9178551541", from_="3475148471", url="http://3bbq.localtunnel.com/xml/")
	
    # sid = call.sid
    # call = client.calls.get(sid)
	
    # print call.notifications.list()
    # print call.recordsings.list()
    # print call.transcriptions.list()
    return HttpResponse(request)
