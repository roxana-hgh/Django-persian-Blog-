from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']

class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']