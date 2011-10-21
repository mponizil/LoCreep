from django.conf.urls.defaults import *

from django.contrib import admin

from lc.locreep import app, twil, util

urlpatterns = patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/opt/bitnami/apps/django/django_projects/test_site/static'}),
	
	(r'^$', util.welcome_pg),
	(r'^welcome$', util.welcome_pg),
	(r'^register$', util.register),
	(r'^login$', util.login_pg),
	(r'^auth$', util.auth),
	(r'^logout$', util.logout_pg),
	
	(r'^dashboard$', app.dashboard),
	(r'^groups/(\d+)$', app.group),
	(r'^groups/create$', app.create_group),
	(r'^groups/save$', app.save_group),
	(r'^conversations/(\d+)$', app.conversation),
    
    (r'^user_message$', app.user_message),
    
    (r'^text$', twil.text),
	(r'^phone$', twil.phone),
	(r'^save_creepy_voice$', twil.save_creepy_voice),
	
	(r'^tumblr_text$', util.tumblr_text),
	
    url(r'^admin', include(admin.site.urls)),
)
