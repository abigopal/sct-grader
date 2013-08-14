from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Member(models.Model):
    user = models.OneToOneField(User, related_name='member')
    goes_to_tj = models.BooleanField(default=False) #is the student from tj
    tj_username = models.CharField(max_length=30)
    activation = models.CharField(max_length=30)
    tj_activation = models.CharField(max_length=30)
    
    @python_2_unicode_compatible
    def __str__(self):
        return '<Member %s>' % self.user.username

    class Meta:
        app_label = 'grader'
    

class Team(models.Model):
    teamname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    leader = models.ForeignKey(User, related_name='+')
    members = models.ManyToManyField(Member, related_name='members')

    @python_2_unicode_compatible
    def __str__(self):
        return '<Team %s>' % self.teamname

    class Meta:
        app_label = 'grader'
