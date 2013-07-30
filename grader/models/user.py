from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    activated = models.BooleanField(default=False) #user is new. have admins check if tj student
    tj = models.BooleanField(default=False) #is the student from tj
    
    @python_2_unicode_compatible
    def __str__(self):
        return '<User %s>' % self.username

    class Meta:
        app_label = 'grader'
    

class Team(models.Model):
    teamname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    leader = models.ForeignKey(User, related_name='+')
    members = models.ManyToManyField(User, related_name='members')

    @python_2_unicode_compatible
    def __str__(self):
        return '<User %s>' % self.teamname

    class Meta:
        app_label = 'grader'
