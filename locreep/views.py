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

domain_name = "http://3bbq.localtunnel.com"



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

#def tumblr_text(request):
def tumblr_text(request, title, body):
#    title = "html post"
#    body = "<p style='color:green'> paragraph </p> <center> centered stuff </center>"

    title = urlparse.unquote(title)
    body = urlparse.unquote(body)

    api = Api(BLOG,USER,PASSWORD)
    post = api.write_regular(title,body)
    return HttpResponse(title + "\n" + body)

def myGroups(request):
    html=''

    html+='<b>Groups</b>'

    groups = Group.objects.filter(users=request.user) #lets say this is all groups i belong to
    rows=0
    html+='<table>'
    for i in groups:
        if rows%4==0:
            html+='<tr>'
        html+='<td><a href="/group/?id='+str(i.id)+'/"><img src = "'+str(i.photo)+'" style="height:50px;width:50px"></a></td>'

        if rows%4==3:
            html += '</tr>'

        rows+=1
    if rows%4!=0:
        html += '</tr>'

    html+= '</table>'
    html+='<a href="/newGroup/">New Group</a>'

    return HttpResponse(html)

def group(request):

    html=''

    html+='<b>Members</b>'
    g = Group.objects.filter(id=request.GET['id']) #lets say this is all groups i belong to
    members = User.objects.filter(group=g)
    html+='<table>'

    for i in members:
        html+='<tr>'
        html+='<td>'+i.name+'</td>'
        html+='</tr>'

    html+='</table>'

    html+='<b>Creeps</b>'
    creeps = Creep.objects.filter(group=g)

    rows=0
    html+='<table>'
    for i in groups:
        if rows%4==0:
            html+='<tr>'
        html+='<td><a href="/creep/'+i.id+'/"><img src = "'+i.photo+'" style="height:50px;width:50px"></a></td>'
        if rows%4==3:
            html += '</tr>'

        rows+=1

    if rows%4!=0:
        html += '</tr>'

    html+= '</table>'

    html+='<a href="/invite/'+request.GET['id']+'/">Invite</a>'

    return HttpResponse(html)

