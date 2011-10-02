from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from locreep import views

urlpatterns = patterns('',
	(r'^$', views.welcome),
	(r'^text/$', views.text),
	
    #(r'^create/$', views.create),
    #(r'^myGroups/$', views.myGroups),
    #(r'^confirmInvite/(\d{1,2})/$', views.confirmInvite),

	(r'^save_creepy_voice/$', views.save_creepy_voice),
	(r'^phone/$', views.phone),
	
	#(r'^search/$', views.search),
	#(r'^groups/$', views.groups),
	#(r'^creeps/$', views.creeps),
    url(r'^admin/', include(admin.site.urls)),
	(r'^tumblr_text/(.*)/(.*)$', views.tumblr_text),
)
