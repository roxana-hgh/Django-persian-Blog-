from django import forms
from django.forms import ModelForm
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','body','image','category']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'instagram_url', 'twitter_url', 'linkedin_url', 'website_url']
  
    

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']
  