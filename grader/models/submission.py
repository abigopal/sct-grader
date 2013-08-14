from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from .user import Member, Team
from .contest import Problem 

class Submission(models.Model):
    user = models.ForeignKey(Member)
    prob = models.ForeignKey(Problem)
    solved = models.BooleanField(default=False)
    lang = models.CharField(max_length=10)
    submitted = models.DateTimeField()
    submission = models.TextField()

    @python_2_unicode_compatible
    def __str__(self):
        return '<Submission %s %s>' % (self.user, self.prob)

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
