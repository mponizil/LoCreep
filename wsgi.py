import os
import sys

sys.path.append('/srv/locreep/lib/python2.6/site-packages/')
os.environ["DJANGO_SETTINGS_MODULE"] = "lc.settings"
path = '/srv/locreep/'
if path not in sys.path:
    sys.path.append(path)
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
