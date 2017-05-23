from django import forms
from .models import Company
from home.models import JobinTerritory


class NewCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ('is_new', 'logo',)


class EditCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ('is_new', 'logo', 'user', 'email', 'points')
