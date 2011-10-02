from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from locreep import views

urlpatterns = patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/opt/bitnami/apps/django/django_projects/test_site/static'}),
	(r'^$', views.welcome),
	(r'^welcome/$', views.welcome),
	(r'^login/$', views.login),
	
	(r'^text/$', views.text),
	
    #(r'^create/$', views.create),
    #(r'^myGroups/$', views.myGroups),
    #(r'^confirmInvite/(\d{1,2})/$', views.confirmInvite),
    
    (r'^creep/(\d+)$', views.creep),
    (r'^user_message/$', views.user_message),

	(r'^save_creepy_voice/$', views.save_creepy_voice),
	(r'^phone/$', views.phone),
	
	(r'^tumblr_text/$', views.tumblr_text),
	
	#(r'^search/$', views.search),
	#(r'^groups/$', views.groups),
	#(r'^creeps/$', views.creeps),
    url(r'^admin/', include(admin.site.urls)),

    (r'^myGroups/$', views.myGroups),
    (r'^groupies/$', views.groupies),
)
