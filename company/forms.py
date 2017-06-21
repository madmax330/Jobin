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


class NewSuggestionForm(forms.ModelForm):

    class Meta:
        model = Suggestion
        fields = ('company', 'topic', 'suggestion', 'importance')

