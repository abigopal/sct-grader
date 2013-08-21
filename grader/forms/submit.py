from django import forms

class SubmitForm(forms.Form):
    programming_languages = (
        ('java', 'Java'),
        ('C++11', 'C++ 11'),
        ('C++03', 'C++ 03'),
        ('C', 'C'),
        ('Python', 'Python'),
    )
    lang = forms.ChoiceField(choices=programming_languages)
    problem = forms.ChoiceField(choices=[])
    upload = forms.FileField()
