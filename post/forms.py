from django import forms
from .models import Post
from home.models import JobinProgram


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
            'deadline': 'Application Deadline',
            'wage': 'Wage $/hr',
            'cover_instructions': 'Enter some instructions for the cover letter here'
        }