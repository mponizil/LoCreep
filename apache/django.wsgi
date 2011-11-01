import os
import sys
 
sys.path.append('/srv/www')
sys.path.append('/srv/www/lc')
sys.path.append('/srv/www/lc/locreep')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'lc.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
