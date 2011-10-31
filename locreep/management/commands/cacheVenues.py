from django.core.management.base import BaseCommand, CommandError
from locreep.models import *
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

def objectify(results):
  for j in results:
    if j:
      o = json.loads(j)
      for i in o['response']['groups'][0]['items']:
        filt=Venue.objects.filter(fourSqId=i['id'])
        if not filt:
          p=Venue(latitude=str(i['location']['lat']), longitude=str(i['location']['lng']),fourSqId=i['id'], points=0)
          p.save()


class Command(BaseCommand):
  def handle(self, *args, **options):
    categories={
    'General Entertainment' : '4bf58dd8d48988d1f1931735',
    'Arts & Entertainment' : '4d4b7104d754a06370d81259',
    'Performing Arts Venue' : '4bf58dd8d48988d1f2931735',
    'Music Venue' : '4bf58dd8d48988d1d9941735',
    'Strip Club' : '4bf58dd8d48988d1d6941735',
    'College & University' : '4d4b7105d754a06372d81259',
    'Fraternity House' : '4bf58dd8d48988d1b0941735',
    'Sorority House' : '4bf58dd8d48988d141941735',
    'Nightlife Spot' : '4d4b7105d754a06376d81259',
    'Nightclub' : '4bf58dd8d48988d11f941735',
    'Other Nightlife' : '4bf58dd8d48988d11a941735',
    'Pub' : '4bf58dd8d48988d11b941735',
    'Religious Center' : '4bf58dd8d48988d131941735'
    }

    north = (40.804645,-73.973351)
    east = (40.770853,-73.940048)
    west = (40.770333, -74.008369)
    south = (40.714147,-73.989143)

    width=abs((west[1]-east[1])/10)
    height=abs((north[0]-south[0])/20)

    results=[]
    for cat in categories:
      for i in range(0,10):
        for j in range(0,20):
          url='https://api.foursquare.com/v2/venues/search?ll=' + str(40.714147+(j*height)) + ',' + str(-74.008369+(i*width))+'&categoryId='+categories[cat]+'&oauth_token=VQ4HZXAPPQWRSART3RCRKE3GAIYU2IEBU02Q5H4XI0QOL1PS'
          results.append(tryUrl(url))

    objectify(results)
