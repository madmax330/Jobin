from django import forms
from . models import Resume, Language, Experience, Award, School, Skill


class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ['name', 'file_resume', 'gpa', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-half'}),
            'gpa': forms.TextInput(attrs={'class': 'w3-input w3-half'}),
            'is_active': forms.Select(attrs={'class': 'w3-input w3-half'},
                                      choices=(
                                          ('false', 'False'),
                                          ('true', 'True'),
                                      )),
        }


class NewResumeForm(forms.ModelForm):

    class Meta:
        model = Resume
        fields = ['name', 'gpa', 'is_active']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input w3-half'}),
            'gpa': forms.TextInput(attrs={'class': 'w3-input w3-half'}),
            'is_active': forms.Select(attrs={'class': 'w3-input w3-half'},
                                      choices=(
                                          ('false', 'False'),
                                          ('true', 'True'),
                                      )),
        }
        labels = {
            'is_active': 'Make Active Resume'
        }


class LanguageForm(forms.ModelForm):

    class Meta:
        model = Language
        fields = ['name', 'level']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input'}),
            'level': forms.Select(attrs={'class': 'w3-input w3-half'},
                                  choices=(
                                      ('native', 'Native'),
                                      ('fluent', 'Fluent'),
                                      ('conversational', 'Conversational'),
                                      ('beginner', 'Beginner'),
                                  )),
        }


class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ['title', 'start', 'end', 'company', 'description', 'experience_type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input'}),
            'start': forms.DateInput(attrs={'class': 'w3-input w3-third', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'w3-input w3-third present', 'type': 'date'}),
            'company': forms.TextInput(attrs={'class': 'w3-input'}),
            'description': forms.Textarea(attrs={'class': 'w3-input'}),
            'experience_type': forms.Select(attrs={'class': 'w3-input w3-half'},
                                            choices=(
                                                  ('professional', 'Professional'),
                                                  ('academic', 'Academic'),
                                                  ('internship', 'Internship'),
                                                  ('volunteer', 'Volunteer'),
                                                  ('entrepreneurial', 'Entrepreneurial'),
                                                  ('other', 'Other'),
                                            )),
        }


class AwardForm(forms.ModelForm):

    class Meta:
        model = Award
        fields = ['title', 'date', 'description', 'award_type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w3-input'}),
            'date': forms.DateInput(attrs={'class': 'w3-input w3-third', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'w3-input'}),
            'award_type': forms.TextInput(attrs={'class': 'w3-input'})
        }


class SchoolForm(forms.ModelForm):

    class Meta:
        model = School
        fields = ['name', 'program', 'start', 'end', 'level']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input'}),
            'program': forms.TextInput(attrs={'class': 'w3-input'}),
            'start': forms.DateInput(attrs={'class': 'w3-input w3-third', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'w3-input w3-third present', 'type': 'date'}),
            'level': forms.Select(attrs={'class': 'w3-input w3-half'},
                                  choices=(
                                      ('university', 'University'),
                                      ('college', 'College'),
                                      ('high school', 'High School'),
                                      ('other', 'Other')
                                  )),
        }

        labels = {
            'name': 'School Name'
        }


class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill
        fields = ['name', 'level']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'w3-input'}),
            'level': forms.Select(attrs={'class': 'w3-input w3-half'},
                                  choices=(
                                      ('beginner', 'Beginner'),
                                      ('intermediate', 'Intermediate'),
                                      ('advanced', 'Advanced'),
                                  )),
        }

