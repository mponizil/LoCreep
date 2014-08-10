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

import re

try:
    from local_settings import *
except ImportError:
    pass
account = TWILIO_ACCOUNT_SID
token = TWILIO_AUTH_TOKEN
tc = TwilioRestClient(account, token)

@login_required(login_url='/login')
def dashboard(request):
    try:
        groups = Group.objects.filter(members=request.user)
    except Group.DoesNotExist:
        groups = None

    return render_to_response("dashboard.html", { 'groups': groups }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def group(request, group_id):
    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return render_to_response("error.html", { 'error': "No group found." })

    try:
        membership = Membership.objects.get(user=request.user,group=group,is_leader=True)
        is_leader = True
    except Membership.DoesNotExist:
        is_leader = False

    membership = Membership.objects.filter(group=group).exclude(user__password='')
    member_count = membership.count()

    return render_to_response("group.html", { 'group': group, 'member_count': member_count, 'is_leader': is_leader }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def view_members(request, group_id):
    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return render_to_response("error.html", { 'error': "No group found." })

    try:
        membership = Membership.objects.get(user=request.user,group=group,is_leader=True)
        is_leader = True
    except Membership.DoesNotExist:
        is_leader = False

    return render_to_response("view-members.html", { 'group': group, 'is_leader': is_leader }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def view_creeps(request, group_id):
    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return render_to_response("error.html", { 'error': "no group found" })

    conversations = Conversation.objects.filter(group=group)

    return render_to_response("view-creeps.html", { 'group': group, 'conversations': conversations }, context_instance=RequestContext(request))

@login_required(login_url='/login')
def create_group(request):
    number = Number.objects.filter(is_available=True)

    if number.count() == 0:
        return render_to_response("error.html", { 'error': "We apologize but we are fresh out of numbers to give out. Try again soon; we are working on obtaining more." })

    if not request.user.is_active:
        return render_to_response("error.html", { 'error': "We apologize but we are going to need you to validate your email address before you can create a group.<br /><br /><a href='/send-again'>Send confirmation email again</a>" }, context_instance=RequestContext(request))

    return render_to_response("create-group.html", { 'phone': number[0].phone }, context_instance=RequestContext(request))

@csrf_exempt
@require_POST
def save_group(request):
    name = request.POST['name']
    phone = request.POST['phone']

    # see if user is group leader of any groups
    membership = Membership.objects.filter(user=request.user,is_leader=True)
    if membership.count() > 0:
        return HttpResponse('{ "success": false, "error": "You may only create one group." }')

    # create new group
    group = Group(name=name,phone=phone)
    group.save()

    # create user membership as leader
    membership = Membership.objects.create(user=request.user,group=group,is_leader=True)

    # make the phone number unavailable
    try:
        number = Number.objects.get(phone=phone,is_available=True)
    except Number.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "We apologize but we are fresh out of numbers to give out. Try again soon; we are working on obtaining more." }')
    number.is_available = False
    number.save()

    return HttpResponse('{ "success": true, "data": { "group_id": ' + str(group.id) + ' } }')

@csrf_exempt
@require_POST
def delete_group(request, group_id):
    # make sure group exists and user is a member
    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "Group does not exist." }')

    try:
        membership = Membership.objects.get(user=request.user,group=group,is_leader=True)
    except Membership.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "You are not leader of this group." }')

    group.delete()

    number = Number.objects.get(phone=group.phone)
    number.is_available = True
    number.save()

    return HttpResponse('{ "success": true }')

@login_required(login_url='/login')
def add_friends(request, group_id):
    try:
        group = Group.objects.get(id=group_id,members=request.user)
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
        return render_to_response("error.html", { 'error': "Invalid invite link. No user found." })

    # check if user has a password
    if user.password:
        return render_to_response("error.html", { 'error': "Invalid invite link. User already registered." })

    # make sure they're really in the group the link says they're in
    try:
        group = Group.objects.get(id=group_id,members=user)
    except Group.DoesNotExist:
        return render_to_response("error.html", { 'error': "Invalid invite link. No group found with user." })

    return render_to_response("added-by-email.html", { 'user': user, 'group': group })

@login_required(login_url='/login')
def conversation(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return render_to_response("error.html", { 'error': "No conversation found." })

    try:
        group = Group.objects.get(conversation=conversation,members=request.user)
    except Group.DoesNotExist:
        return render_to_response("error.html", { 'error': "No conversation found." })

    messages = Message.objects.filter(conversation=conversation).order_by('-id')

    longUrl = urllib.quote_plus('http://locreep.com/conversation/' + str(conversation.id))
    f = urllib2.urlopen('http://api.bitly.com/v3/shorten?login=afcampa&apiKey=R_a2e5411ee02dc84186802a509dfb4ced&longUrl='+longUrl+'%2F&format=json')
    a = json.loads(f.read())
    qr = a['data']['url']+'.qrcode'

    return render_to_response("conversation.html", { 'conversation': conversation, 'creep': conversation.creep, 'messages': messages, 'qr': qr }, context_instance=RequestContext(request))

@csrf_exempt
@require_POST
def search(request):
    friend = request.POST['friend']
    group_id = request.POST['group_id']

    users = User.objects.filter(Q(username__icontains=friend) | Q(first_name__icontains=friend) | Q(last_name__icontains=friend)).exclude(id=request.user.id)
    users_found = []
    for user in users:
        in_group = Group.objects.filter(id=group_id,members=user).exists()
        users_found.append({ 'id': user.id, 'photo': user.userprofile.photo, 'name': user.get_full_name(), 'email': user.username, 'in_group': in_group })

    return HttpResponse(json.dumps(users_found))

@csrf_exempt
@require_POST
def add_member(request):
    group_id = request.POST['group_id']
    user_id = request.POST['user_id']

    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "Not authorized." }')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "User not found." }')

    # max users in a group is 5
    membership = Membership.objects.filter(group=group)
    if membership.count() >= 5:
        return HttpResponse('{ "success": false, "error": "Only 5 users to a group." }')

    # check if membership exists
    membership = Membership.objects.filter(user=user,group=group)
    if membership.count() >= 1:
        return HttpResponse('{ "success": false, "error": "User is already in this group." }')

    # create new membership
    membership = Membership.objects.create(user=user,group=group,is_leader=False)

    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def delete_member(request, group_id, user_id):
    # check if user to be deleted exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "No user found." }')

    # check if group exists with user to be deleted as member
    try:
        group = Group.objects.get(id=group_id,members=user)
    except Group.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "No group found." }')

    # check if request.user is leader
    try:
        membership = Membership.objects.get(user=request.user,group=group,is_leader=True)
        if user == request.user:
            return HttpResponse('{ "success": false, "error": "The leader cannot be deleted from their own group." }')
    except Membership.DoesNotExist:
        if user == request.user:
            membership = Membership.objects.get(user=user,group=group)
        else:
            return HttpResponse('{ "success": false, "error": "You are not leader of this group." }')

    # delete membership
    membership = Membership.objects.get(user=user,group=group)
    membership.delete()

    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def add_email(request):
    group_id = request.POST['group_id']
    invited_by_id = request.POST['invited_by_id']
    email = request.POST['email']

    smtp_server = 'smtp.gmail.com:587'
    from_addr = 'invites@locreep.com'

    # make sure user is actually in this group
    try:
        group = Group.objects.get(id=group_id,members=request.user)
    except Group.DoesNotExist:
        return HttpResponse('{ "success": false, "error": "not authorized" }')

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        invited_by = User.objects.get(id=invited_by_id)
        invited_by_name = invited_by.get_full_name()
        link = "http://locreep.com/groups/" + str(group_id) + "/added-by-email?email=" + email

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
        server.login('invites@locreep.com','locreeper')
        server.sendmail(from_addr, email, msg.as_string())
        server.quit()
        # email sent

        user = User(username=email)
        user.save()

    # check if membership exists
    membership = Membership.objects.filter(user=user,group=group)
    if membership.count() >= 1:
        return HttpResponse('{ "success": false, "error": "User is already in this group." }')

    # create new membership
    membership = Membership.objects.create(user=user,group=group,is_leader=False)

    return HttpResponse('{ "success": true }')

@csrf_exempt
@require_POST
def user_message(request):
    conversation_id = request.POST['conversation_id']

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return render_to_response("error.html", { 'error': "no conversation" })

    user = request.user
    body = request.POST['body']

    message = Message(conversation=conversation,user_type='user',user=user,body=body)
    message.save()

    url = 'http://locreep.com:3000/message'
    values = {'conversation_id' : conversation_id,
              'user_type' : 'user',
              'message' : body }
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    sms = tc.sms.messages.create(to = conversation.creep.phone, from_ = conversation.group.phone, body = body)

    return HttpResponse('{ "success": true }')

@login_required(login_url='/login')
def creep_lookup(request):
    return render_to_response("creep-lookup.html", context_instance=RequestContext(request))

@csrf_exempt
@require_POST
def reverse_lookup(request):
    number = request.POST['number']
    number = re.sub("\D", "", number)

    try:
        creep = Creep.objects.get(phone__icontains=number)
        creep_phone = creep.phone
        conversations = Conversation.objects.filter(creep=creep)
        messages = Message.objects.filter(creep=creep)
        c_hits = conversations.count()
        m_hits = messages.count()
    except Creep.DoesNotExist:
        creep_phone = number
        c_hits = 0
        m_hits = 0

    return HttpResponse('{ "number": "' + creep_phone + '", "c_hits": ' + str(c_hits) + ', "m_hits": ' + str(m_hits) + ' }')
