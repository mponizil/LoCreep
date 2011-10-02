from django.db import models

class User(models.Model):
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    fname = models.CharField()
    lname = models.CharField()
    def __unicode__(self):
        return self.fname

class Group(models.Model):
    phone = models.IntegerField(max_length = 10)

    def __unicode__(self):
        return self.phone

class UserInGroups(models.Model):
    user_id = models.ForeignKey(User)
    group_id = models.ForeignKey(Group)

    def __unicode__(self):
        return self.id

class Creep(models.Model):
    phone = models.IntegerField(max_length = 10)
    photo = models.CharField(max_length = 75)
    last_seen = models.CharField(max_length = 255)
    
    def __unicode__(self):
        return self.phone

class Conversation(models.Model):
    group_id = models.ForeignKey(Group)
    creep_id = models.ForeignKey(Creep)
    tumblr_id = models.CharField(max_length = 255)
    qr_id = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.group_id

class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length = 10)
    user_id = models.ForeignKey(User)
    creep_id = models.ForeignKey(Creep)

    def __unicode__(self):
        return self.phone