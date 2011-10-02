from django.db import models

class User(models.Model):
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    fname = models.CharField(max_length = 20)
    lname = models.CharField(max_length = 20)
    def __unicode__(self):
        return self.fname

class Group(models.Model):
    name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 12)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class UserInGroups(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    confirmed = models.BooleanField()

    def __unicode__(self):
        return self.id

class Creep(models.Model):
    phone = models.CharField(max_length = 12)
    photo = models.CharField(max_length = 75)
    last_seen = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.phone

class Conversation(models.Model):
    group = models.ForeignKey(Group)
    creep = models.ForeignKey(Creep)
    tumblr_id = models.CharField(max_length = 255, null = True)
    qr_id = models.CharField(max_length = 255, null = True)

    def __unicode__(self):
        return self.id

class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length = 10)
    user = models.ForeignKey(User, null = True)
    creep = models.ForeignKey(Creep, null = True)

    def __unicode__(self):
        return self.id