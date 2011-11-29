from django.core.management.base import BaseCommand, CommandError

from locreep.models import *
from datetime import datetime
import json
import urllib2

class Command(BaseCommand):
  def handle(self, *args, **options):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = "https://api.twilio.com"
        password_mgr.add_password(None, top_level_url, 'ACb77594eb2632a2d77422086328ef03a9', '536e78251ae04f88ce7828ecd66fc673')
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        
        url = 'https://api.twilio.com/2010-04-01/Accounts/ACb77594eb2632a2d77422086328ef03a9/IncomingPhoneNumbers.json?PageSize=250'
        request = urllib2.Request(url)
        response = opener.open(request)
        data = response.read()
        numbers = json.loads(data)['incoming_phone_numbers']
        
        i = 1
        
        for number in numbers:
            print '{\n  "model": "locreep.number",\n  "pk": ' + str(i) + ',\n  "fields": {\n    "phone":"' + number['phone_number'] + '"\n  }\n},'
            
            i += 1