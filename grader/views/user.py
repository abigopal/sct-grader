from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from grader.models import Member

class DashboardView(View):
    template = '../templates/dashboard.djhtml'

    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        user = request.user.member
        first_name = request.user.first_name
        return render(request, self.template, {'username':username,
                                               'first_name': first_name,})
