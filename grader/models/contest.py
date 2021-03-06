from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

from .score import Entry
from .user import Member, Team
# Create your models here.

class Problem(models.Model):
    title = models.CharField(max_length=30)
    letter = models.CharField(max_length=1)
    points = models.IntegerField()
    evaluator = models.CharField(max_length=30)
    flags = models.CharField(max_length=30)
    memory_limit = models.IntegerField()
    time_limit = models.IntegerField()

    @python_2_unicode_compatible
    def __str__(self):
        return '<Problem %s>' % self.title

    def clean(self):
        self.letter = self.letter.capitalize()

    class Meta:
        app_label = 'grader'

class TestCase(models.Model):
    inp = models.TextField()
    out = models.TextField()
    num = models.IntegerField()
    problem = models.ForeignKey(Problem, related_name='test_cases')

    @python_2_unicode_compatible
    def __str__(self):
        return '<TestCase %s>' % self.num

    class Meta:
        app_label = 'grader'
        ordering = ('num',)

class Subtask(models.Model):
    num = models.IntegerField(default=0)
    points = models.IntegerField()
    test_cases = models.CommaSeparatedIntegerField(max_length=100)
    problem = models.ForeignKey(Problem, related_name='subtasks')

    @python_2_unicode_compatible
    def __str__(self):
        return '<Subtask %s %s>' % (self.problem, self.num)

    class Meta:
        app_label = 'grader'

class Contest(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    total_points = models.IntegerField()
    registered = models.ManyToManyField('Member', through='Entry')
    problems = models.ManyToManyField(Problem)
    start = models.DateTimeField()
    end = models.DateTimeField()
    active = models.BooleanField(default=False)
    
    def _is_over(self):
        if self.end < now():
            return True
        return False

    def _has_started(self):
        if self.start < now():
            return True
        return False

    is_over = property(_is_over)
    has_started = property(_has_started)
    @python_2_unicode_compatible
    def __str__(self):
        return '<Contest %s>' % self.name

    class Meta:
        app_label = 'grader'
        ordering = ('-start',)
'''
Once again this code seems really redundant,
and I the reason for writing it this way
isn't really obvious. But it's done this
way for a reason. I will probably go back
and abstract a lot of this out.

-AG
'''

class TeamContest(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    prob_file = models.CharField(max_length=30)
    total_points = models.IntegerField()
    registered = models.ManyToManyField('Team', through='TeamEntry')
    problems = models.ManyToManyField(Problem)
    complete = models.BooleanField(default=False) # Contest is over; show submissions.
    start = models.DateTimeField()
    end = models.DateTimeField()
    @python_2_unicode_compatible
    def __str__(self):
        return '<TeamContest %s>' % self.name

    class Meta:
        app_label = 'grader'
        abstract = False
