from django.core.management.base import BaseCommand, CommandError
from geiger.meter.models import *
import json
import urllib2

#should we store the herenows to backtrack the creeps?
#do we get speed enhancement if we use 4sq api multis?
#has to handle bad reqs
def tryUrl(url):
  try:
    j=urllib2.urlopen(url)
  except urllib2.HTTPError, e:
    j=tryUrl(url)
    return
  else:
    return j.read()

class Command(BaseCommand):
  #args = '<poll_id poll_id ...>'
  #help = 'Updates venue creeppoints'
  def handle(self, *args, **options):
    venues=Venue.objects.all()
    creeps=Creep.objects.all()
    for venue in venues:
      url='https://api.foursquare.com/v2/venues/'+venue.fourSqId+'/herenow?oauth_token=VQ4HZXAPPQWRSART3RCRKE3GAIYU2IEBU02Q5H4XI0QOL1PS'
      result=tryUrl(url)
      obj=json.loads(result)
      idList=[]
      for person in obj['response']['hereNow']['items']:
        idList.append(person['id'])
      for creep in creeps:
        if creep.fourSqId in idList:
          c=CreepPoint(place=venue)
          c.save()
          venue.points=venue.points+1
          venue.save()
