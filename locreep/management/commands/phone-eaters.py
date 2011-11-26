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
        # get all the inactive users
        users = User.objects.filter(is_active=False)
        match = 0
        
        # iterate through inactive users to find which of them run groups
        for user in users:
            # find the membership object of group where the user is a leader
            m = Membership.objects.filter(user=user,is_leader=True)
            
            if len(m) > 0:
                # this user needs to verify their email dammit
                
                # get their registration key
                rk = RegistrationKey.objects.get(user=user)
                
                # prepare and send the email
                # email requesting that user validate email
                smtp_server = 'smtp.gmail.com:587'
                from_addr = 'admin@locreep.com'

                # send email requesting they validate their address
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Please validate your email address"
                msg['From'] = 'LoCreep Admin'
                msg['To'] = user.email

                link = "http://locreep.com/valid-email/" + rk.rand_str

                text = "Hello LoCreeper,\n\nWe are writing to notify you that you have created a group on LoCreep but have yet to validate your email address. In order to keep the number we assigned your group, we're going to need you to verify. Please navigate to the following link to verify your account. Thank you!\n\n" + link + "\n\nHappy creeping!\nThe LoCreep Team"
                html = "<html><head></head><body>Hello LoCreeper,<br /><br />We are writing to notify you that you have created a group on LoCreep but have yet to validate your email address. In order to keep the number we assigned your group, we're going to need you to verify. Please navigate to the following link to verify your account. Thank you!<br /><br /><a href='" + link + "'>" + link + "</a><br /><br />Happy creeping!<br />The LoCreep Team</body></html>"

                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')

                msg.attach(part1)
                msg.attach(part2)

                server = smtplib.SMTP(smtp_server)
                server.starttls()
                
                print 'send email to: ' + user.email
                print 'with link: ' + link
                print str(match) + '\n'
                
                server.login('admin@locreep.com','locreeper')
                server.sendmail(from_addr, user.email, msg.as_string())
                server.quit()