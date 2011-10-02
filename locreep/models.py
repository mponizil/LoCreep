from django.db import models

class User(models.Model):
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    def __unicode__(self):
        return self.fname

class Group(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField(max_length=10)
    description = models.TextField()
    creeps = models.ManyToManyField(Creep, verbose_name="creeps in a group")
    users = models.ManyToManyField(User, verbose_name="users in a group") 

    def __unicode__(self):
        return self.name

class Creep(models.Model):
    phone = models.IntegerField(max_length=10)
    photo = models.CharField(max_length=75)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.phone

class Conversation(models.Model):
    group = models.ForeignKey(Group, verbose_name="group this conversation belongs to")
    creep = models.ForeignKey(Creep, verbose_name="creep this conversation belongs to")
    tumblr_id = models.CharField(max_length=255)
    qr_id = models.CharField(max_length=255)

    def __unicode__(self):
        return self.group_id

class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length=10)
    user = models.ForeignKey(User)
    creep = models.ForeignKey(Creep)

    def __unicode__(self):
        return self.conversation_id
