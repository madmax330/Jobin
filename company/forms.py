from django import forms
from .models import Company, Suggestion


class NewCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ('is_new', 'logo',)


class EditCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        exclude = ('is_new', 'logo', 'user', 'email', 'points')


IMAGE_EXTENSIONS = ['jpeg', 'jpg', 'gif', 'png']


class UploadLogoForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ('logo',)

    def clean(self):
        clean_data = super(UploadLogoForm, self).clean()
        file = clean_data['logo']
        if file.size > 512 * 1024:
            raise forms.ValidationError({'logo': 'The file size cannot exceed 512KBs.'})
        arr = file.name.split('.')
        ext = arr[len(arr) - 1]
        if not len(arr) > 1:
            raise forms.ValidationError({'logo': 'The file extension is not recognized.'})
        if not (ext in IMAGE_EXTENSIONS):
            raise forms.ValidationError({'logo': 'The file must be a jpeg, jpg, gif or png.'})


class NewSuggestionForm(forms.ModelForm):

    class Meta:
        model = Suggestion
        fields = ('company', 'topic', 'suggestion', 'importance')

