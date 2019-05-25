from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.CharField(max_length=50, required=False, help_text='Optional.')
    question = forms.CharField(max_length=50, required=False, help_text='Optional.')
    answer = forms.CharField(max_length=50, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'email', 'question', 'answer', )