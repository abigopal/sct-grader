from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.contenttypes.models import ContentType

class Entry(models.Model):
    user = models.ForeignKey('Member')
    contest = models.ForeignKey('Contest')
    total_score = models.IntegerField(default=0)

    @python_2_unicode_compatible
    def __str__(self):
        return '<Entry %s %s>' % (self.contest, self.user)

    class Meta:
        app_label = 'grader'

class ProblemScore(models.Model):
    letter = models.CharField(max_length=1)
    points = models.IntegerField(default=0)
    entry = models.ForeignKey(Entry, related_name='problem_score')
    last_submit = models.DateTimeField(auto_now=True)

    @python_2_unicode_compatible
    def __str__(self):
        return '<ProblemScore %s>' % self.letter

    class Meta:
        app_label = 'grader'

class SubtaskScore(models.Model): 
    num = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)
    problem_score = models.ForeignKey(ProblemScore, related_name='subtask_score')

    @python_2_unicode_compatible
    def __str__(self):
        return '<SubtaskScore %s>' % self.num

    class Meta:
        app_label = 'grader'
'''
This portion of the code may seem really redundant. 
I chose not to use GenericForeignKeys, because 
that may lead to some compatibility issues
(i.e. we decide to add some random information
for team entries only) later. I'll probably go
through and abstract a lot of this out later.

-AG
'''

class TeamEntry(models.Model):
    team = models.ForeignKey('Team')
    contest = models.ForeignKey('TeamContest')
    total_score = models.IntegerField()

    @python_2_unicode_compatible
    def __str__(self):
        return '<TeamEntry %s %s>' % (self.contest, self.team)

    class Meta:
        app_label = 'grader'

class TeamProblemScore(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    entry = models.ForeignKey(TeamEntry)
    last_submit = models.DateTimeField(auto_now=True)

    @python_2_unicode_compatible
    def __str__(self):
        return '<TeamProblemScore %s>' % self.name

    class Meta:
        app_label = 'grader'

class TeamSubtaskScore(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    complete = models.BooleanField()
    problem = models.ForeignKey(TeamProblemScore)

    @python_2_unicode_compatible
    def __str__(self):
        return '<TeamSubtaskScore %s>' % self.name

    class Meta:
        app_label = 'grader'
