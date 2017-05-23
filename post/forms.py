from django import forms
from .models import Post, Application
import datetime


class NewPostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('schools', 'status', 'supplied_by_jobin', 'notified', 'new_apps')

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


class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('company', 'schools', 'status', 'supplied_by_jobin', 'notified', 'new_apps', 'is_startup_post')

    def clean(self):
        clean_data = super(EditPostForm, self).clean()
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


class NewApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('post', 'student', 'resume', 'date', 'status', 'post_title', 'student_name')


class AddCoverLetterForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('cover', 'cover_submitted',)


class ChangeResumeForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('resume',)







