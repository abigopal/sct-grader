from django import forms
from django.contrib.auth.models import User

from grader.models import Member

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    tj_username = forms.CharField(max_length=11, required=False, label="*TJ username")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name', '')
        if not data:
            raise forms.ValidationError('Missing first name.')
        if not data.isalpha():
            raise forms.ValidationError('First names can have numbers and letters only.')
        if len(data) < 2:
            raise forms.ValidationError('First names must be longer than one letter.')
        data = data.title()
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name', '')
        if not data:
            raise forms.ValidationError('Missing last name.')
        if not data.isalpha():
            raise forms.ValidationError('Last names can have numbers and letters only.')
        if len(data) < 2:
            raise forms.ValidationError('Last names must be longer than one letter.')
        data = data.title()
        return data

    def clean_tj_username(self): #TODO: check if username exists 
        data = self.cleaned_data.get('tj_username', '')
        if data:
            if len(data) < 7:
                raise forms.ValidationError('Invalid TJ Username.')
            years = ['2014', '2015', '2016', '2017'] #TODO: put this in settings
            if data[:4] not in years:
                raise forms.ValidationError('Invalid TJ Username.') #TODO: add more robustness 
        return data

    def clean_username(self):
        data = self.cleaned_data.get('username', '')
        print data
        if not data:
            raise forms.ValidationError('Missing username.')
        if len(data) < 3:
            raise forms.ValidationError('Usernames must be greater than three characters.')
        if not data.isalnum():
            raise forms.ValidationError('Users must be alphanumeric.')
        if User.objects.filter(username__iexact=data).exists():
            raise forms.ValidationError('Username already exists.')
        return data

    def clean_email(self):
        data = self.cleaned_data.get('email', '')
        if not data:
            raise forms.ValidationError('Missing email.')
        if User.objects.filter(email__iexact=data).exists():
            raise forms.ValidationError('Email already exists.')
        return data #NB: EmailField uses a "moderately complex" regexp to take care of the trickiness.

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        data = cleaned_data.get('password', '')
        if not data:
            raise forms.ValidationError('Missing password.')
        data2 = cleaned_data.get('confirm_password', '')
        if not data2:
            raise forms.ValidationError('Missing password confirmation.')
        if data2 != data:
            raise forms.ValidationError('Passwords don\'t match.')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
