from django.core.management import setup_environ
import settings

setup_environ(settings)

from locreep.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random, string

users = User.objects.all()[0:200]

for user in users:
    if not user.email:
        # user.delete()
        print 'deleting user without email\n'
    else:
        # set user is_active to False
        user.is_active = False
        # user.save()
        print 'deactivating user: ' + user.email

        # create RegistrationKey
        rand_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(12))
        registration_key = RegistrationKey(rand_str=rand_str,user=user)
        # registration_key.save()
        print 'creating registration key: ' + rand_str

        # email requesting that user validate email
        smtp_server = 'smtp.gmail.com:587'
        from_addr = 'admin@locreep.com'

        # send email requesting they validate their address
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Please validate your email address"
        msg['From'] = 'LoCreep Admin'
        msg['To'] = user.email

        link = "http://locreep.com/valid-email/" + rand_str

        text = "Hello LoCreeper,\n\nThanks for joining LoCreep, we are happy to have you on board! There are new features brewing, so stick around as we assemble the world's first Creeper prevention software.\n\nBefore becoming a card-carrying LoCreep user, we need you to validate your email in order to use the tools and receive a LoCreep phone number. Please click the following link to validate your email address. Thank you!\n\n" + link + "\n\nHappy creeping!\nThe LoCreep Team"
        html = "<html><head></head><body>Hello LoCreeper,<br /><br />Thanks for joining LoCreep, we are happy to have you on board! There are new features brewing, so stick around as we assemble the world's first Creeper prevention software.<br /><br />Before becoming a card-carrying LoCreep user, we need you to validate your email in order to use the tools and receive a LoCreep phone number. Please click the following link to validate your email address. Thank you!<br /><br /><a href='" + link + "'>" + link + "</a><br /><br />Happy creeping!<br />The LoCreep Team</body></html>"

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        server = smtplib.SMTP(smtp_server)
        server.starttls()
        server.login('admin@locreep.com','locreeper')
        # server.sendmail(from_addr, user.email, msg.as_string())
        server.quit()
        print 'email sent\n'
        # email sent