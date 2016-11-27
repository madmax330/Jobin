from django import forms
from .models import Event
from home.models import JobinTerritory


class NewEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            'title', 'date', 'time', 'address', 'city', 'state', 'zipcode', 'country',
            'website', 'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'w3-input w3-half'},
                                  choices=JobinTerritory.objects.values_list('name', 'name')),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'w3-input w3-half'},
                                    choices=JobinTerritory.objects.values_list('country', 'country').distinct()),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'date': 'Event Date (mm/dd/yyyy)',
            'time': 'Event Time (hh : mm AM/PM)',
        }