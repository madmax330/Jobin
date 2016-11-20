from django import forms
from .models import Post
from home.models import JobinProgram
import datetime


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title','programs', 'type', 'wage', 'openings', 'start_date',
            'end_date', 'deadline', 'description', 'requirements', 'cover_instructions'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'},
                                 choices=(
                                      ('newgrad', 'New Grad'),
                                      ('volunteer', 'Volunteer'),
                                      ('internship', 'Internship'),
                                      ('parttime', 'Part-Time'),
                                  )),
            'wage': forms.TextInput(attrs={'class': 'form-control'}),
            'openings': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control'}),
            'programs': forms.Select(attrs={'class': 'form-control'}, choices=JobinProgram.objects.values_list('name', 'name')),
            'cover_instructions': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'deadline': 'Application Deadline (mm/dd/yyyy)',
            'wage': 'Wage $/hr',
            'cover_instructions': 'Enter some instructions for the cover letter here',
            'start_date': 'Start Date (mm/dd/yyyy)',
            'end_date': 'End Date (mm/dd/yyyy)',
        }

    def clean(self):
        clean_data = super(NewPostForm, self).clean()
        start = clean_data.get('start_date')
        end = clean_data.get('end_date')
        dead = clean_data.get('deadline')
        today = datetime.datetime.now().date()
        if (start < today) or (dead < today):
            raise forms.ValidationError({'start_date': "The start and deadline date cannot be before today's date."})
        if end:
            if end < start:
                raise forms.ValidationError({'start_date': 'The start date must be before end date.'})
            if end < dead:
                raise forms.ValidationError({'deadline': 'The deadline must be before end date.'})
        if start < dead:
            raise forms.ValidationError({'deadline': 'The deadline must be before the start date.'})












