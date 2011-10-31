from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.CharField(max_length=75, default="/static/images/users/anonymous.jpg")
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    post_save.connect(create_user_profile, sender=User)
    
    def __unicode__(self):
        return str(self.user.username)

class Creep(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=12)
    photo = models.CharField(max_length=75, default="/static/images/creeps/anonymous.jpg")
    name = models.CharField(max_length=75, default="Name Unknown")

    def __unicode__(self):
        return str(self.phone)

class Group(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=75, blank=True, default="/static/images/groups/anonymous.jpg")
    phone = models.CharField(max_length=12)
    creeps = models.ManyToManyField(Creep, verbose_name="creeps in a group", null=True, blank=True)
    users = models.ManyToManyField(User, verbose_name="users in a group")

    def __unicode__(self):
        return self.name

class Conversation(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, verbose_name="group this conversation belongs to", null=True, blank=True)
    creep = models.ForeignKey(Creep, verbose_name="creep this conversation belongs to", null=True, blank=True)
    notes = models.TextField(blank=True, default="Make a note")
    tumblr_id = models.CharField(max_length=255, blank=True)
    qr_id = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return str(self.group.name) + ": " + str(self.id)

class Message(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length=10)
    user = models.ForeignKey(User, null=True)
    creep = models.ForeignKey(Creep, null=True)
    body = models.TextField()

    def __unicode__(self):
        return str(self.body)[:10]

class Number(models.Model):
    phone = models.CharField(max_length=12)
    is_available = models.BooleanField()
    
    def __unicode__(self):
        return str(self.phone)