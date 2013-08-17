from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from grader.models import Contest, Problem, Entry, ProblemScore, SubtaskScore

def entry_exists(user, contest):
    qs = Entry.objects.filter(contest=contest, user=user)
    return qs.exists()

class ContestPage(View):
    template = '../templates/contest_page.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        contest_slug = kwargs['contest']
        contest = get_object_or_404(Contest, active=True, slug=contest_slug)
        user = request.user.member
        problems = contest.problems.all()

        if entry_exists(user, contest):
            return render(request, self.template, {'contest': contest, 'problems':problems}) #render the page
        entry = Entry(user=user, contest=contest)
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
        return render(request, self.template, {'contest':contest, 'problems':problems})

class ProblemPage(View):
    template = '../templates/problem_page.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        contest_slug = kwargs['contest']
        problem_slug = kwargs['problem']

        contest = get_object_or_404(Contest, active=True, slug=contest_slug)
        user = request.user.member 
        if not entry_exists(user, contest):
            HttpRedirect('/contest-gateway')

        problem = get_object_or_404(Problem, slug=problem_slug)

        if problem not in contest.problems.all():
            raise Http404

        return render(request, self.template, {'problem':problem})

