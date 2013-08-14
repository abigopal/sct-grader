from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from grader.forms.auth import RegistrationForm, LoginForm
from grader.models import Contest

from datetime import datetime
class ContestGateway(View):
    template = '../templates/gateway.html'
    
    @method_decorator(login_required)
    def get(self, request):
        now = datetime.now()
        qs = Contest.objects.filter(active=True, end__gte=now, start__lte=now)
        contests = list(qs)
        return render(request, self.template, {'contests':contests})

