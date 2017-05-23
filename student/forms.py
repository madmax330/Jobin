from django import forms
from .models import Student


class NewStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('is_new',)


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('is_new', 'user', 'school',)
