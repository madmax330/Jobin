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
        fields = ['title', 'start', 'end', 'company', 'description', 'experience_type', 'is_current']

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
            'is_current': forms.TextInput(attrs={'id': 'curr-in', 'value': 'False'}),
        }

        labels = {
            'is_current': 'hide',
        }

    def clean(self):
        clean_data = super(ExperienceForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


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
        fields = ['name', 'program', 'start', 'end', 'level', 'is_current']

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
            'is_current': forms.TextInput(attrs={'id': 'curr-in', 'value': 'False'}),
        }

        labels = {
            'name': 'School Name',
            'is_current': 'hide'
        }

    def clean(self):
        clean_data = super(SchoolForm, self).clean()
        end = clean_data.get('end')
        curr = clean_data.get('is_current')
        if curr == 'False':
            if not end:
                raise forms.ValidationError({'end': "End date must be specified if this isn't your current position."})
        if end:
            start = clean_data.get('start')
            if end < start:
                raise forms.ValidationError({'start': 'Start date must be before end date.'})


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

