from django import forms
from .models import Company
from home.models import JobinTerritory

class NewCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'address', 'city', 'state', 'zipcode', 'country',
                  'phone', 'logo', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinTerritory.objects.values_list('name', 'name')),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinTerritory.objects.values_list('country', 'country').distinct()),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
        }