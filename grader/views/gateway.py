from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from grader.forms.auth import RegistrationForm, LoginForm
from grader.models import Contest

class ContestGatewayView(View):
    template = '../templates/gateway.djhtml'
    
    @method_decorator(login_required)
    def get(self, request):
        qs = Contest.objects.filter(active=True) #!!!: Trippy
        contests = list(qs)
        user = request.user.member
        first_name = request.user.first_name
        return render(request, self.template, {'contests':contests,
                                               'first_name': first_name,})

