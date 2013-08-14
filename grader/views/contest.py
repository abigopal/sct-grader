from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from grader.models import Contest, Entry

def entry_exists(user, contest):
    qs = Entry.objects.filter(contest=contest, user=user)
    return qs.exists()

class ContestPage(View):
    template = '../templates/contest_page.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        url_contest = kwargs['contest']
        contest = get_object_or_404(Contest, active=True, slug=url_contest)
        user = request.user.member
        problems = list(contest.problems.all())
        if entry_exists(user, contest):
            return render(request, self.template, {'problems':problems}) #render the page
        entry = Entry(user=user, contest=contest)
        entry.save()
        for p in problems:
            ps = ProblemScore()
            ps.letter = p.letter
            ps.entry = entry
            ps.save()
            
            for st in p.subtasks:
                sts = SubtaskScore()
                sts.num = st.num
                sts.save()
                sts.problem_score = ps

        # stupid scoring stuff here 
