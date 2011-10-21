from django.conf.urls.defaults import *

from django.contrib import admin

from lc.locreep import app, twil, util

urlpatterns = patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/opt/bitnami/apps/django/django_projects/test_site/static'}),
	
	(r'^$', util.welcome),
	(r'^welcome$', util.welcome),
	(r'^register$', util.register),
	(r'^login$', util.login),
	(r'^auth$', util.auth),
	
	(r'^dashboard$', app.dashboard),
	(r'^group/(\d+)$', app.group),
	(r'^conversation/(\d+)$', app.conversation),
    
    (r'^user_message$', app.user_message),
    
    (r'^text$', twil.text),
	(r'^phone$', twil.phone),
	(r'^save_creepy_voice$', twil.save_creepy_voice),
	
	(r'^tumblr_text$', util.tumblr_text),
	
    url(r'^admin', include(admin.site.urls)),
)
