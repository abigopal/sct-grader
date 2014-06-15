from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from grader.forms.auth import RegistrationForm, LoginForm, ChangePasswordForm
from grader.models import Member

import random
import string 
import os

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
        
        path_to_user_home = os.path.join(settings.MEDIA_ROOT, 'users', username)
        os.mkdir(path_to_user_home)
        
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
            return HttpResponseRedirect(reverse('contest-gateway', args=[]))
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, self.template, {'form':form})
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('contest-gateway', args=[]))
            else:
                e = 'User is suspended.'
                return render(request, self.template, {'form':form, 
                                                       'login_message':e,})
        else:
            e = 'Invalid login.'
            return render(request, self.template, {'form':form, 
                                                   'login_message':e,})

    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('contest-gateway', args=[]))
        form = self.form()
        return render(request, self.template, {'form':form})

class LogoutView(View):
    form = LoginForm
    template = '../templates/login.djhtml'

    @method_decorator(login_required)
    def post(self, request):
        form = self.form()
        logout(request)
        msg = 'Logged out successfully!'
        return render(request, self.template, {'form':form,
                                               'login_message':msg,})

    @method_decorator(login_required)
    def get(self, request):
        form = self.form()
        logout(request)
        msg = 'Logged out successfully!'
        return render(request, self.template, {'form':form, 
                                               'login_message':msg,})

class ChangePasswordView(View):
    form = ChangePasswordForm
    template = '../templates/dashboard.djhtml'
    
    @method_decorator(login_required)
    def post(self, request):
        form = self.form(request.POST)
        user = request.user
        first_name = user.first_name
        if not form.is_valid():
            msg = 'Invaild form.'
            return render(request, self.template, {'change_password_form':form,
                                                   'change_password_message': msg,
                                                   'first_name':first_name,})
        current_password = form.cleaned_data['current_password']
        new_password = form.cleaned_data['new_password']
        confirm_new_password = form.cleaned_data['confirm_new_password']

        if new_password != confirm_new_password:
            msg = 'Passwords don\'t match.'
            return render(request, self.template, {'change_password_form':form,
                                                   'change_password_error': msg,
                                                   'first_name':first_name,})

        if not request.user.check_password(current_password):
            msg = 'Old password isn\'t correct.'
            return render(request, self.template, {'change_password_form':form,
                                                   'change_password_error':msg,
                                                   'first_name':first_name,})
        user.set_password(new_password)
        user.save()
        msg = 'Password changed successfully!'
        return render(request, self.template, {'change_password_form':form,
                                               'change_password_message':msg,
                                               'first_name':first_name,})
