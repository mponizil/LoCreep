from django.core.management.base import BaseCommand, CommandError

from locreep.models import *
from django.contrib.auth.models import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import re

import random, string

class Command(BaseCommand):
  def handle(self, *args, **options):
        users = User.objects.all()[0:80]
        
        for user in users:
            # email requesting that user validate email
            smtp_server = 'smtp.gmail.com:587'
            from_addr = 'admin@locreep.com'

            # send email requesting they validate their address
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "LoCreep will be down until further notice"
            msg['From'] = 'LoCreep Admin'
            msg['To'] = user.email
            
            text = "Dear " + user.first_name + ",\n\nAs you may or may not be aware, LoCreep all began at HackNY's Fall 24-Hour Hackathon. The initial product was built in one night and then polished briefly for presentation at the New York Tech Meetup. After amazing feedback from our user base, LoCreep continued to receive attention and the team made plans to see if the fun little hack could become something bigger.\n\nIt has been decided that a bit of a facelift is in order. For the next couple of months, LoCreep will go into stealth mode as we prepare Version 1.0 of what we believe will turn the dating game on its head.\n\nUnfortunately, the phone numbers we have given out will no longer be in service and the groups you have made will be lost. We thank you for your participation and patience and will notify you as soon as LoCreep is ready for prime time. In the mean time, you will just have to hold the creeps off by your own inner strength until we return.\n\nSincerely,\nThe LoCreep Team"
            
            html = "<html><head></head><body>Dear " + user.first_name + ",<br /><br />As you may or may not be aware, LoCreep all began at HackNY's Fall 24-Hour Hackathon. The initial product was built in one night and then polished briefly for presentation at the New York Tech Meetup. After amazing feedback from our user base, LoCreep continued to receive attention and the team made plans to see if the fun little hack could become something bigger.<br /><br />It has been decided that a bit of a facelift is in order. For the next couple of months, LoCreep will go into stealth mode as we prepare Version 1.0 of what we believe will turn the dating game on its head.<br /><br />Unfortunately, the phone numbers we have given out will no longer be in service and the groups you have made will be lost. We thank you for your participation and patience and will notify you as soon as LoCreep is ready for prime time. In the mean time, you will just have to hold the creeps off by your own inner strength until we return.<br /><br />Sincerely,<br />The LoCreep Team</body></html>"

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            server = smtplib.SMTP(smtp_server)
            server.starttls()
            server.login('admin@locreep.com','locreeper')
            server.sendmail(from_addr, user.email, msg.as_string())
            server.quit()
            print 'email sent\n'
            # email sent