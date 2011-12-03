from django.conf.urls.defaults import *

urlpatterns = patterns('locreep.views',
    url(r'^valid-email/(\w+)$', 'util.valid_email'),
    url(r'^send-again$', 'util.send_again'),
    
    url(r'^$', 'util.welcome_pg'),
    url(r'^welcome$', 'util.welcome_pg'),
    url(r'^register$', 'util.register'),
    url(r'^login$', 'util.login_pg'),
    url(r'^auth$', 'util.auth'),
    url(r'^logout$', 'util.logout_pg'),
    url(r'^users/update$', 'util.update_user'),
    
    url(r'^dashboard$', 'app.dashboard'),
    
    url(r'^groups/create$', 'app.create_group'),
    url(r'^groups/save$', 'app.save_group'),
    
    url(r'^groups/(\d+)$', 'app.group'),
    url(r'^groups/(\d+)/members$', 'app.view_members'),
    url(r'^groups/(\d+)/creeps$', 'app.view_creeps'),
    url(r'^groups/(\d+)/add-friends$', 'app.add_friends'),
    url(r'^groups/(\d+)/added-by-email$', 'app.added_by_email'),
    url(r'^groups/(\d+)/delete$', 'app.delete_group'),
    url(r'^groups/(\d+)/users/(\d+)/delete$', 'app.delete_member'),
    
    url(r'^users/search$', 'app.search'),
    url(r'^groups/add-member$', 'app.add_member'),
    url(r'^groups/add-email$', 'app.add_email'),
    
    url(r'^conversations/(\d+)$', 'app.conversation'),
    
    url(r'^user_message$', 'app.user_message'),
    
    url(r'^text$', 'twil.text'),
    url(r'^phone$', 'twil.phone'),
    url(r'^save_creepy_voice$', 'twil.save_creepy_voice'),
    
    url(r'^tumblr_text$', 'util.tumblr_text'),
    
    url(r'^gauge$', 'gauge.home'),
    url(r'^locate$', 'gauge.locate'),
    
    url(r'^upload/creep_photo$', 'img.upload_creep_photo'),
    
    url(r'^creep-lookup$', 'app.creep_lookup'),
    url(r'^reverse-lookup$', 'app.reverse_lookup'),
    
    url(r'^video$', 'static.video'),
    url(r'^how-to$', 'static.how_to'),
    url(r'^terms$', 'static.terms'),
    url(r'^contact$', 'static.contact'),
    url(r'^press$', 'static.press'),
)