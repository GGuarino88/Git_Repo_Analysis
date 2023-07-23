from django import forms
from django.forms import ModelForm
from .models import Scan, User_Scans


class ScanForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-field',
        'type': 'text',
        'placeholder': 'Enter Title',

    }))

    class Meta:
        model = Scan
        fields = ['title', ]


class UserScanForm(ModelForm):
    repo_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-field',
        'type': 'text',
        'placeholder': 'Enter Repository Name'

    }))

    url_name = forms.URLField(widget=forms.TextInput(attrs={
        'class': 'form-field',
        'type': 'text',
        'placeholder': 'Enter Repository URL'

    }))

    class Meta:
        model = User_Scans
        fields = ['repo_name', 'url_name']