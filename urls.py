from django.conf.urls.defaults import *
from lc.locreep import views

urlpatterns = patterns('',
	(r'^$', views.welcome),
	(r'^phone/$', views.phone),
	(r'^text/$', views.text),
)