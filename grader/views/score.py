from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from grader.models import Contest, Problem, Entry, ProblemScore, SubtaskScore

def sort_by_score(a, b):
    diff = b.total_score - a.total_score
    if diff == 0:
        if a.last_submit < b.last_submit:
            return -1
        elif a.last_submit > b.last_submit:
            return 1
        else:
            return 0
    return int(diff)
        
class ScoreboardView(View):
    template = '../templates/scoreboard.djhtml'
    
    @method_decorator(login_required)
    def get(self, request,  *args, **kwargs):
        contest_slug = kwargs['contest']
        contest = get_object_or_404(Contest, active=True, slug=contest_slug)
        username = request.user.username
        first_name = request.user.first_name
        entries = contest.entries.all()
        problems = contest.problems.all()
        sorted_entries = sorted(entries, cmp=sort_by_score)
        sorted_problems = sorted(problems, key=lambda problem: problem.letter)
        return render(request, self.template, {'problems': sorted_problems,
                                               'entries' : sorted_entries,
                                               'username'    : username,
                                               'first_name':first_name,})
