from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    tj = models.BooleanField(default=True) #is the student from tj

    @python_2_unicode_compatible
    def __str__(self):
        return '<User %s>' % self.username


class Team(models.Model):
    teamname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    leader = models.ForeignKey(User)
    members = models.ManyToManyField(User)

    @python_2_unicode_compatible
    def __str__(self):
        return '<User %s>' % self.teamname
