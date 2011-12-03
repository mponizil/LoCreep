from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.CharField(max_length=75, default="/static/images/users/anonymous.jpg")
    
    def __unicode__(self):
        return str(self.user.username)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)

class RegistrationKey(models.Model):
    rand_str = models.CharField(max_length=12)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return str(self.user.email + ": " + self.rand_str)

class Creep(models.Model):
    date_created = models.DateTimeField()
    phone = models.CharField(max_length=12)
    photo = models.CharField(max_length=75, default="/static/images/creeps/anonymous.jpg")
    name = models.CharField(max_length=75, default="Name Unknown")
    fourSqId = models.CharField(max_length=200, blank=True)
    
    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        super(Creep, self).save()
    
    def __unicode__(self):
        return str(self.phone)

class Group(models.Model):
    date_created = models.DateTimeField()
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=75, blank=True, default="/static/images/groups/anonymous.jpg")
    phone = models.CharField(max_length=12)
    creeps = models.ManyToManyField(Creep, verbose_name="creeps in a group", null=True, blank=True)
    members = models.ManyToManyField(User, through="Membership")
    
    def save(self):
        if self.date_created == None:
            self.date_created = datetime.now()
        super(Group, self).save()
    
    def __unicode__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_leader = models.BooleanField(default=False)
    
    def __unicode__(self):
        leader = ""
        if self.is_leader:
            leader = " (Leader)"
        return str(self.group.name) + ": " + str(self.user.username) + str(leader)

class Conversation(models.Model):
    date_created = models.DateTimeField()
    group = models.ForeignKey(Group, verbose_name="group this conversation belongs to", null=True, blank=True)
    creep = models.ForeignKey(Creep, verbose_name="creep this conversation belongs to", null=True, blank=True)
    notes = models.TextField(blank=True, default="Make a note")
    tumblr_id = models.CharField(max_length=255, blank=True)
    qr_id = models.CharField(max_length=255, blank=True)
    
    def save(self):
        if self.date_created == None:
          self.date_created = datetime.now()
        super(Conversation, self).save()
    
    def __unicode__(self):
        return str(self.group.name) + ": " + str(self.id)

class Message(models.Model):
    date_created = models.DateTimeField()
    conversation = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length=10)
    user = models.ForeignKey(User, null=True)
    creep = models.ForeignKey(Creep, null=True)
    body = models.TextField()
    
    def save(self):
        if self.date_created == None:
          self.date_created = datetime.now()
        super(Message, self).save()
    
    def __unicode__(self):
        return str(self.body)[:10]

class Number(models.Model):
    phone = models.CharField(max_length=12)
    is_available = models.BooleanField(default=True)
    
    def __unicode__(self):
        return str(self.phone) + " (" + str(self.is_available) + ")"

class Venue(models.Model):
    latitude  = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    fourSqId  = models.CharField(max_length=200)
    points = models.IntegerField()

    # for future robustness
    # points = models.ForeignKey(CreepPoints)

class CreepPoint(models.Model):
    place = models.ForeignKey(Venue)
    time = models.DateField(auto_now=True)