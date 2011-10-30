from locreep.models import *

from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from twilio.rest import TwilioRestClient
from twilio import twiml

from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.views.decorators.http import require_POST

import urllib
import urllib2
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

account = "ACb77594eb2632a2d77422086328ef03a9"
token = "536e78251ae04f88ce7828ecd66fc673"
tc = TwilioRestClient(account, token)

@login_required(login_url='/login')
def dashboard(request):
    try:
        groups = Group.objects.filter(users=request.user)
    except Group.DoesNotExist:
        groups = None
    
    return render_to_response("dashboard.html", { 'groups': groups }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return HttpResponse("no group found")
    
    conversations = Conversation.objects.filter(group=group)
    
    return render_to_response("group.html", { 'group': group, 'conversations': conversations }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def create_group(request):
    number = Number.objects.filter(is_available=True)
    return render_to_response("create-group.html", { 'phone': number[0].phone }, context_instance=RequestContext(request))

@csrf_exempt
def save_group(request):
    name = request.POST['name']
    description = request.POST['description']
    phone = request.POST['phone']
    
    # create new group
    g = Group(name=name,description=description,phone=phone)
    g.save()
    
    # add current user to the group
    g.users.add(request.user)
    
    # make the phone number unavailable
    number = Number.objects.get(phone=phone)
    number.is_available = False
    number.save()
    
    return HttpResponse('{ "success": true, "data": { "group_id": ' + str(g.id) + ' } }')

@login_required(login_url='/login')
def add_friends(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        group = None
    
    return render_to_response("add-friends.html", { 'group': group }, context_instance=RequestContext(request))

def added_by_email(request, group_id):
    email = request.GET['email']
    
    # if user is logged in, redirect them to dashboard
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    
    # make sure user has been invited
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return HttpResponse("invalid invite link. no user found.")
    
    # check if user has a password
    if user.password:
        return HttpResponse("invalid invite link. user already registered.")
    
    # make sure they're really in the group the link says they're in
    try:
        group = Group.objects.get(id=group_id,users=user)
    except Group.DoesNotExist:
        return HttpResponse("invalid invite link. no group found with user.")
    
    return render_to_response("added-by-email.html", { 'user': user, 'group': group })

@login_required(login_url='/login')
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
    
    return render_to_response("conversation.html", { 'conversation_id': conversation.id, 'group_id': conversation.group.id, 'creep': conversation.creep, 'messages': messages, 'qr': qr }, context_instance=RequestContext(request))

@csrf_exempt
@require_POST
def search(request):
    friend = request.POST['friend']
    group_id = request.POST['group_id']
    
    users = User.objects.filter(Q(username__icontains=friend) | Q(first_name__icontains=friend) | Q(last_name__icontains=friend)).exclude(id=request.user.id)
    u = []
    for user in users:
        in_group = Group.objects.filter(id=group_id,users=user).exists()
        u.append({ 'id': user.id, 'name': user.get_full_name(), 'email': user.username, 'in_group': in_group })
    
    return HttpResponse(json.dumps(u))

@csrf_exempt
@require_POST
def add_user(request):
    group_id = request.POST['group_id']
    user_id = request.POST['user_id']
    
    group = Group.objects.get(id=group_id)
    user = User.objects.get(id=user_id)
    
    group.users.add(user)
    
    return HttpResponse('{ "success": true }')
    
@csrf_exempt
@require_POST
def add_email(request):
    group_id = request.POST['group_id']
    invited_by_id = request.POST['invited_by_id']
    email = request.POST['email']
    
    smtp_server = 'smtp.gmail.com:587'
    from_addr = 'misha.ponizil@gmail.com'
    
    group = Group.objects.get(id=group_id)
    
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        invited_by = User.objects.get(id=invited_by_id)
        invited_by_name = invited_by.get_full_name()
        link = "http://localhost:8000/groups/" + str(group_id) + "/added-by-email?email=" + email
        
        # send email inviting user to join locreep
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Join my group on LoCreep"
        msg['From'] = from_addr
        msg['To'] = email
        
        text = invited_by_name + " wants you to join their group on LoCreep. Follow the link provided to get started!\n\n" + link
        html = "<html><head></head><body>" + invited_by_name + " wants you to join their group on LoCreep. Follow the link provided to get started!<br /><br /><a href='" + link + "'>" + link + "</a></body></html>"
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login('misha.ponizil','series36')
        server.sendmail(from_addr, email, msg.as_string())
        server.quit()
        # email sent
        
        user = User(username=email)
        user.save()
    
    group.users.add(user)

    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def user_message(request):
    conversation_id = request.POST['conversation_id']
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return HttpResponse('no conversation')

    user = request.user
    body = request.POST['body']

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