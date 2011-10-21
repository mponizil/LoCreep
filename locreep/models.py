from django.db import models

class User(models.Model):
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)

    def __unicode__(self):
        return self.fname

class Creep(models.Model):
    phone = models.CharField(max_length=12)
    photo = models.CharField(max_length=75)
    name = models.CharField(max_length=75)

    def __unicode__(self):
        return str(self.phone)

class Group(models.Model):
    name = models.CharField(max_length=30)
    photo = models.CharField(max_length=75, null=True)
    phone = models.CharField(max_length=12)
    description = models.TextField()
    creeps = models.ManyToManyField(Creep, verbose_name="creeps in a group")
    users = models.ManyToManyField(User, verbose_name="users in a group")

    def __unicode__(self):
        return self.name

class Conversation(models.Model):
    group = models.ForeignKey(Group, verbose_name="group this conversation belongs to")
    creep = models.ForeignKey(Creep, verbose_name="creep this conversation belongs to")
    tumblr_id = models.CharField(max_length=255, null=True)
    qr_id = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return str(self.id)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    user_type = models.CharField(max_length=10)
    user = models.ForeignKey(User, null=True)
    creep = models.ForeignKey(Creep, null=True)
    body = models.TextField()

    def __unicode__(self):
        return str(self.id)
