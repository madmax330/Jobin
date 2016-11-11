from django import forms
from .models import Student
from home.models import JobinSchool, JobinMajor, JobinProgram, JobinTerritory


class NewStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'firstname', 'lastname', 'dob', 'phone', 'school', 'program', 'major',
            'graduate', 'address', 'city', 'state', 'zipcode', 'country', 'linkedin', 'work_eligible'
        ]

        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'w3-input'}),
            'lastname': forms.TextInput(attrs={'class': 'w3-input'}),
            'phone': forms.TextInput(attrs={'class': 'w3-input'}),
            'address': forms.TextInput(attrs={'class': 'w3-input'}),
            'city': forms.TextInput(attrs={'class': 'w3-input'}),
            'state': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinTerritory.objects.values_list('name', 'name')),
            'zipcode': forms.TextInput(attrs={'class': 'w3-input'}),
            'country': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinTerritory.objects.values_list('country', 'country').distinct()),
            'school': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinSchool.objects.values_list('name', 'name')),
            'program': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinProgram.objects.values_list('name', 'name')),
            'major': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinMajor.objects.values_list('name', 'name')),
            'graduate': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=(('TRUE', 'True'), ('FALSE', 'False'))),
            'dob': forms.DateInput(attrs={'class': 'w3-input w3-quarter', 'type': 'date'}),
            'linkedin': forms.TextInput(attrs={'class': 'w3-input'}),
            'work_eligible': forms.Select(attrs={'class': 'w3-input w3-half'},
                                     choices=(('TRUE', 'Yes'), ('FALSE', 'No'))),
        }

        labels = {
            'firstname': 'First Name',
            'lastname': 'Last Name',
            'work_eligible': 'Are you legally eligible to work?',
            'dob': 'Date of birth (mm/dd/yyyy)',
        }
