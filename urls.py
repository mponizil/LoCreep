from django.conf.urls.defaults import *
from locreep.foodfinder import views

urlpatterns = patterns('',
	(r'^$', views.welcome),
	(r'^phone/$', views.phone),
	(r'^text/$', views.text),
)