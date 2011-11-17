from locreep.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random, string

def ping_users(request):
    ret = ''
    if request.user.id == 1:
        users = User.objects.all()

        for user in users:
            if not user.email:
                user.delete()
            else:
                # set user is_active to False
                user.is_active = False
                # user.save()
                ret += 'deactivating user: ' + user.email + '<br />'
    
                # create RegistrationKey
                rand_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(12))
                registration_key = RegistrationKey(rand_str=rand_str,user=user)
                registration_key.save()
                ret += 'creating registration key: ' + rand_str + '<br />'
    
                # email requesting that user validate email
                smtp_server = 'smtp.gmail.com:587'
                from_addr = 'admin@locreep.com'

                # send email requesting they validate their address
                msg = MIMEMultipart('alternative')
                msg['Subject'] = "Please validate your email address"
                msg['From'] = 'LoCreep Admin'
                msg['To'] = user.email
        
                link = "http://locreep.com/valid-email/" + rand_str
    
                text = "Hello LoCreeper,\n\nThanks for joining LoCreep, we are happy to have you on board! There are new features brewing, so stick around as we assemble the world's first Creeper prevention software.\n\nIn the mean time, we have a limited supply of phone numbers to give out and we need you to validate your email in order to user the service. Please click the following link to validate your email address.\n\n" + link
                html = "<html><head></head><body>Hello LoCreeper,<br /><br />Thanks for joining LoCreep, we are happy to have you on board! There are new features brewing, so stick around as we assemble the world's first Creeper prevention software.<br /><br />In the mean time, we have a limited supply of phone numbers to give out and we need you to validate your email in order to user the service. Please click the following link to validate your email address.<br /><br /><a href='" + link + "'>" + link + "</a></body></html>"
    
                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(html, 'html')
        
                msg.attach(part1)
                msg.attach(part2)
    
                server = smtplib.SMTP(smtp_server)
                server.starttls()
                server.login('admin@locreep.com','locreeper')
                # server.sendmail(from_addr, user.email, msg.as_string())
                server.quit()
                ret += 'email sent<br />'
                # email sent
        
        return HttpResponse(ret)
    else:
        return HttpResponse('gtfo')