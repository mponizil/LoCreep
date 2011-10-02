from django.conf.urls.defaults import *
from locreep import views

urlpatterns = patterns('',
	(r'^$', views.welcome),
	(r'^phone/$', views.phone),
	(r'^text/$', views.text),
	
    #(r'^create/$', views.create),
    #(r'^myGroups/$', views.myGroups),
    #(r'^confirmInvite/(\d{1,2})/$', views.confirmInvite),
    
	(r'^twilio/$', views.twilio),
	(r'^myGroups/$', views.myGroups),
	(r'^xml/$', views.xml),
	(r'^call/$', views.call),
	
	#(r'^search/$', views.search),
	#(r'^groups/$', views.groups),
	#(r'^creeps/$', views.creeps),
)
