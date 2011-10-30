from django.contrib import admin
from locreep.models import UserProfile, Group, Creep, Conversation, Message, Number

admin.site.register(UserProfile)
admin.site.register(Group)
admin.site.register(Creep)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(Number)