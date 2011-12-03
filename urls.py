from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/opt/bitnami/apps/django/django_projects/test_site/static'}),
	
    url(r'', include('locreep.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)