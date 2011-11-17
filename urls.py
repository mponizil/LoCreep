from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from lc.locreep import app, twil, util, gauge, img, static, valid

urlpatterns = patterns('',
	# (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/opt/bitnami/apps/django/django_projects/test_site/static'}),
	
	(r'^valid-email/(\w+)$', util.valid_email),
	
	(r'^$', util.welcome_pg),
	(r'^welcome$', util.welcome_pg),
	(r'^register$', util.register),
	(r'^login$', util.login_pg),
	(r'^auth$', util.auth),
	(r'^logout$', util.logout_pg),
	(r'^users/update$', util.update_user),
	
	(r'^dashboard$', app.dashboard),
	
	(r'^groups/create$', app.create_group),
	(r'^groups/save$', app.save_group),
	
	(r'^groups/(\d+)$', app.group),
	(r'^groups/(\d+)/members$', app.view_members),
	(r'^groups/(\d+)/creeps$', app.view_creeps),
	(r'^groups/(\d+)/add-friends$', app.add_friends),
	(r'^groups/(\d+)/added-by-email$', app.added_by_email),
	(r'^groups/(\d+)/delete$', app.delete_group),
	(r'^groups/(\d+)/users/(\d+)/delete$', app.delete_member),
	
	(r'^users/search$', app.search),
	(r'^groups/add-member$', app.add_member),
	(r'^groups/add-email$', app.add_email),
	
	(r'^conversations/(\d+)$', app.conversation),
    
    (r'^user_message$', app.user_message),
    
    (r'^text$', twil.text),
	(r'^phone$', twil.phone),
	(r'^save_creepy_voice$', twil.save_creepy_voice),
	
	(r'^tumblr_text$', util.tumblr_text),
	
	(r'^gauge$', gauge.home),
	(r'^locate$', gauge.locate),
	
	(r'^upload/creep_photo$', img.upload_creep_photo),
	
	(r'^creep-lookup$', app.creep_lookup),
	(r'^reverse-lookup$', app.reverse_lookup),
	
	(r'^video$', static.video),
	(r'^how-to$', static.how_to),
	(r'^terms$', static.terms),
	(r'^contact$', static.contact),
    (r'^press$', static.press),
    
    (r'^valid$', valid.ping_users),
    
    url(r'^admin/', include(admin.site.urls)),
)
