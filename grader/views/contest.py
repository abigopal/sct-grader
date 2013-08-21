from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic.base import View

from grader.models import Contest, Problem, Entry, ProblemScore, SubtaskScore
from grader.forms import SubmitForm

from markdown import markdownFromFile

from StringIO import StringIO

def entry_exists(user, contest):
    qs = Entry.objects.filter(contest=contest, member=user)
    return qs.exists()


class ContestView(View):
    template = '../templates/contest_page.djhtml'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        contest_slug = kwargs['contest']
        contest = get_object_or_404(Contest, active=True, start__lte=now(), slug=contest_slug)
        user = request.user.member
        first_name = request.user.first_name
        problems = contest.problems.all()
        contest_text = ''

        try:
            buff = StringIO()
            index_file = 'grader/contests/' + contest_slug + '/index.md'
            markdownFromFile(input=index_file, output=buff)
            contest_text = buff.getvalue()
        except IOError:
            raise Http404

        formatted_problems = []
        for p in problems:
            try:
                buff = StringIO()
                index_file = 'grader/contests/' + contest_slug + '/' + p.letter + '.md'
                markdownFromFile(input=index_file, output=buff)
                problem_text = buff.getvalue()
            except IOError:
                problem_text = ''
            formatted_problems.append((p.letter, problem_text,))
            
        if entry_exists(user, contest):
            return render(request, self.template, {'contest': contest, 
                                                   'problems':formatted_problems, 
                                                   'contest_text':contest_text,
                                                   'first_name': first_name,}) 

        entry = Entry(member=user, contest=contest)
        entry.save()
        for p in problems:
            ps = ProblemScore()
            ps.letter = p.letter
            ps.entry = entry
            ps.save()
            
            subtasks = p.subtasks.all()
            for st in subtasks:
                sts = SubtaskScore()
                sts.num = st.num
                sts.problem_score = ps
                sts.save()
        return render(request, self.template, {'contest':contest, 
                                               'problems':formatted_problems, 
                                               'contest_text':contest_text,
                                               'first_name': first_name,})

class ProblemView(View):
    template = '../templates/problem_page.djhtml'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        contest_slug = kwargs['contest']
        problem_letter = kwargs['problem']
        problem_text = ''
        contest = get_object_or_404(Contest, active=True, start__lte=now(), slug=contest_slug)
        user = request.user.member 
        first_name = request.user.first_name
        if not entry_exists(user, contest):
            HttpRedirect('/contest-gateway')
        
        problem = get_object_or_404(Problem, letter=problem_letter)

        if problem not in contest.problems.all():
            raise Http404

        
        try:
            buff = StringIO()
            index_file = 'grader/contests/' + contest_slug + '/' + problem_letter + '.md'
            markdownFromFile(input=index_file, output=buff)
            problem_text = buff.getvalue()
        except IOError:
            raise Http404

        return render(request, self.template, {'problem':problem,
                                               'problem_text':problem_text,
                                               'first_name':first_name,})

class SubmitView(View):
    template = '../templates/submit_page.djhtml'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        contest_slug = kwargs['contest']
        contest = get_object_or_404(Contest, active=True, start__lte=now(), end__gte=now(), slug=contest_slug)
        user = request.user.member
        first_name = request.user.first_name
        choices = []
        for p in contest.problems.all():
            letter = p.letter
            name = p.title
            tup = (letter, letter + ': ' + name)
            choices.append(tup)
        if not entry_exists(user, contest):
            HttpRedirect('/contest-gateway')
        form = SubmitForm()
        form.fields['problem'].choices = choices
        form.fields['problem'].initial = choices[0][0] # A contest by definition has at least 1 problem 
        return render(request, self.template, {'form':form,
                                               'first_name':first_name})
