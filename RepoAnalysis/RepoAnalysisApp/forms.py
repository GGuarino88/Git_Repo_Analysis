from django import forms
from django.forms import ModelForm
from .models import Semester, SemesterProject

class SemesterForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'title',
        'type': 'text',
        'placeholder': 'Enter Title',
        'size' : 50
    }))
    class Meta:
        model = Semester
        fields = ['title', ]

class ProjectForm(ModelForm):
    
    team_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'team_name',
        'type': 'text',
        'placeholder': 'Enter Team Name',
        'size' : 50
    }))
    
    repo_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'repo_name',
        'type': 'text',
        'placeholder': 'Enter Project Title',
        'size' : 50
    }))

    url_name = forms.URLField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'url_name',
        'type': 'text',
        'placeholder': 'Enter Repository URL',
        'size' : 50
    }))
    
    class Meta:
        model = SemesterProject
        fields = ['team_name', 'repo_name', 'url_name']