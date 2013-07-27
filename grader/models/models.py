from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
class User(models.Model):
    pass

class Team(models.Model):
    pass

class Problem(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    evaluator = models.CharField(max_length=30)
    flags = models.CharField(max_length=30)
    lang = models.CharField(max_length=100) # JSON encoded array. more efficient than joining.
    
    @python_2_unicode_compatible
    def __str__(self):
        return '<Problem %s>' % self.name

class TestCase(models.Model):
    inp = models.TextField()
    out = models.TextField()
    num = models.IntegerField()
    prob = models.ForeignKey(Problem)

    @python_2_unicode_compatible
    def __str__(self):
        return '<TestCase %s>' % self.num

class Subtask(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    test_cases = models.CommaSeparatedIntegerField(max_length=100)
    prob = models.ForeignKey(Problem)

    @python_2_unicode_compatible
    def __str__(self):
        return '<Subtask %s>' % self.name

class Contest(models.Model):
    name = models.CharField(max_length=30)
    prob_file = models.CharField(max_length=30)
    total_points = models.IntegerField()
    team = models.BooleanField(default=False)
    registered = models.ManyToManyField(User, through='Entry')
    probs = models.ManyToManyField(Problem)

    @python_2_unicode_compatible
    def __str__(self):
        return '<Contest %s>' % self.name

class Entry(models.Model):
    user = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)
    total_score = models.IntegerField()

    @python_2_unicode_compatible
    def __str__(self):
        return '<Entry %s %s>' % (self.contest, self.user)

class ProblemScore(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    entry = models.ForeignKey(Entry)
    last_submit = models.DateField(auto_now=True)

    @python_2_unicode_compatible
    def __str__(self):
        return '<ProblemScore %s>' % self.name
class SubtaskScore(models.Model):
    name = models.CharField(max_length=30)
    points = models.IntegerField()
    complete = models.BooleanField()
    problem = models.ForeignKey(ProblemScore)

    @python_2_unicode_compatible
    def __str__(self):
        return '<SubtaskScore %s>' % self.name


