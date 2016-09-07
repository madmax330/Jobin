from django import forms
from .models import Student
from home.models import JobinSchool, JobinMajor, JobinProgram


class NewStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'firstname', 'lastname', 'dob', 'gender', 'phone',
            'school', 'program', 'major', 'graduate', 'address', 'city', 'state', 'zipcode', 'country'
        ]

        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'w3-input'}),
            'lastname': forms.TextInput(attrs={'class': 'w3-input'}),
            'gender': forms.TextInput(attrs={'class': 'w3-input'}),
            'phone': forms.TextInput(attrs={'class': 'w3-input'}),
            'address': forms.TextInput(attrs={'class': 'w3-input'}),
            'city': forms.TextInput(attrs={'class': 'w3-input'}),
            'state': forms.TextInput(attrs={'class': 'w3-input'}),
            'zipcode': forms.TextInput(attrs={'class': 'w3-input'}),
            'country': forms.TextInput(attrs={'class': 'w3-input'}),
            'school': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinSchool.objects.values_list('name', 'name')),
            'program': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinProgram.objects.values_list('name', 'name')),
            'major': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=JobinMajor.objects.values_list('name', 'name')),
            'graduate': forms.Select(attrs={'class': 'w3-input w3-half'}, choices=(('TRUE', 'True'), ('FALSE', 'False'))),
            'dob': forms.DateInput(attrs={'class': 'w3-input w3-quarter', 'type': 'date'}),
        }
