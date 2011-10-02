from django.contrib import admin
from locreep.models import User, Group, Creep, Conversation, Message

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Creep)
admin.site.register(Conversation)
admin.site.register(Message)
