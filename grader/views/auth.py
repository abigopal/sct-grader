from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from grader.forms.auth import RegistrationForm, LoginForm
from grader.models import Member

import random
import string 

class RegisterView(View):
    form = RegistrationForm
    template = '../templates/register.djhtml'
    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard', args=[]))
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, self.template, {'form':form})
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        tj_username = form.cleaned_data['tj_username']
        
        user = User()
        user.is_active = True #!!!: CHANGE THIS
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.set_password(password)

        user.save()

        activation = self.random_string() #TODO: Add more safety.
        tj_activation = self.random_string() #TODO: Add more safety.
        tj_username = tj_username

        member = Member()
        member.user = user
        member.activation = activation
        member.tj_activation = tj_activation
        member.goes_to_tj = False

        member.save()
        
        return render(request, '../templates/registered_successfully.html', {})

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard', args=[]))
        form = self.form()
        return render(request, self.template, {'form':form})

    def random_string(self, length=20):
        selection = string.ascii_uppercase + string.digits
        return ''.join(random.choice(selection) for x in range(length))

class LoginView(View):
    form = LoginForm
    template = '../templates/login.djhtml'
    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard', args=[]))
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, self.template, {'form':form})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard', args=[]))
            else:
                e = 'User is suspended.'
                return render(request, self.template, {'form':form, 'login_message':e})
        else:
            e = 'Invalid login.'
            return render(request, self.template, {'form':form, 'login_message':e})
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard', args=[]))
        form = self.form()
        return render(request, self.template, {'form':form})

class LogoutView(View):
    form = LoginForm
    template = '../templates/login.djhtml'
    def post(self, request):
        form = self.form()
        logout(request)
        msg = 'Logged out successfully!'
        return render(request, self.template, {'form':form, 'login_message':msg})
    def get(self, request):
        form = self.form()
        logout(request)
        msg = 'Logged out successfully!'
        return render(request, self.template, {'form':form, 'login_message':msg})
