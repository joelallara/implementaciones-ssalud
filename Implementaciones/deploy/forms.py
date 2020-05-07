from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DeployInfo


class DeployForm(forms.ModelForm):
    class Meta:
        model = DeployInfo
        fields = ['lsn']
        widgets = {
            'lsn': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'lsn': '',
        }
