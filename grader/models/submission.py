from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from .user import Member, Team
from .contest import Problem 

import os

# def get_grading_path(username):
#     return os.path.join(settings.MEDIA_ROOT, 'users', 'grading', username)

def get_archive_path(username):
    return os.path.join(settings.MEDIA_ROOT, 'users', username)

class Submission(models.Model):
    user = models.ForeignKey(Member)
    prob = models.ForeignKey(Problem)
    #solved = models.BooleanField(default=False)
    lang = models.CharField(max_length=10)
    submission = models.FileField(upload_to=get_archive_path)
    submitted = models.DateTimeField(auto_now=True)

    @python_2_unicode_compatible
    def __str__(self):
        return '<Submission %s %s>' % (self.user, self.prob)

    class Meta:
        app_label = 'grader'
class TeamSubmission(models.Model): #make visible to all team members
    team = models.ForeignKey(Team)
    prob = models.ForeignKey(Problem)
    solved = models.BooleanField(default=False)
    lang = models.CharField(max_length=10)
    submitted = models.DateTimeField()
    submission = models.TextField()

    @python_2_unicode_compatible
    def __str__(self):
        return '<TeamSubmission %s %s>' % (self.team, self.prob)
