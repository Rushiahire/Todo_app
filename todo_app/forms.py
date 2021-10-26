from django import forms
from django.forms.fields import EmailField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    



class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class TodoForm(forms.Form):
    task = forms.CharField(max_length=20)