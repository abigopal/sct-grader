from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from grader.models import Member

class Dashboard(View):
    template = '../templates/dashboard.html'

    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        return render(request, self.template, {'username':username})
