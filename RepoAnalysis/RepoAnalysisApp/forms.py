from django import forms
from django.forms import ModelForm
from .models import Scan, User_Scans


class ScanForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'title',
        'type': 'text',
        'placeholder': 'Enter Title',
        'size' : 50
    }))

    class Meta:
        model = Scan
        fields = ['title', ]


class UserScanForm(ModelForm):
    repo_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id' : 'repo_name',
        'type': 'text',
        'placeholder': 'Enter Repository Name',
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
        model = User_Scans
        fields = ['repo_name', 'url_name']