from django import forms
from .models import Student


class NewStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('is_new',)


class EditStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        exclude = ('is_new', 'user', 'school', 'email', 'school_requested', 'school_email', 'transcript', 'verified')


class TranscriptForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('transcript',)

    def clean(self):
        clean_data = super(TranscriptForm, self).clean()
        file = clean_data['transcript']
        if file.size > 512 * 1024:
            raise forms.ValidationError({'transcript': 'The file size for your transcript cannot exceed 512Kbs.'})
        arr = file.name.split('.')
        ext = arr[len(arr)-1]
        if not len(arr) > 1:
            raise forms.ValidationError({'transcript': 'The file extension is not recognized. (It must be a PDF)'})
        if not ext.lower() == 'pdf':
            raise forms.ValidationError({'transcript': 'The file must be a PDF.'})
