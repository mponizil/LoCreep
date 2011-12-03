from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import *
import json
import math
from locreep.models import *

# @csrf_exempt
def home(request):
  return render(request, 'gauge.html')

@csrf_exempt
def locate(request):
  max_dist = 1
  lat = request.POST.get('lat') ###post
  lon = request.POST.get('long')
  score=0
  for venue in Venue.objects.all():
    earth_radius=3947 #miles
    dLat=math.radians(float(venue.latitude)-float(lat))
    dLon=math.radians(float(venue.longitude)-float(lon))
    lat1=math.radians(float(lat))
    lat2=math.radians(venue.latitude)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = earth_radius * c
  
    if distance<=max_dist:
      score=score+venue.points
  
  messages={
     0:'This zone is Creeper-free',
    20:'Nothing a bad bitch can\'t handle',
    40:'Get crunk at your own risk',
    60:'Shit just got real',
    80:'Bitches, we gotta get out of here'
    }
  
  if score<20:
    msg=messages[0]
  elif score<40:
    msg=messages[20]
  elif score<60:
    msg=messages[40]
  elif score<80:
    msg=messages[60]
  else:
    msg=messages[80]
  context = {'score':score,'msg':msg}

  return HttpResponse(json.dumps(context))