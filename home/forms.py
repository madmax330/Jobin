from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import JobinBlockedEmail


class NewUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.utype = kwargs.pop('utype', None)
        super(NewUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        clean_data = super(NewUserForm, self).clean()
        if not clean_data.get("username") == clean_data.get("email"):
            raise forms.ValidationError("Username and Email don't match")
        if self.utype == 'student':
            email = clean_data.get("email")
            ext = email.split('@', 1)
            ems = JobinBlockedEmail.objects.filter(extension=ext[1].lower())
            if ems.count() > 1:
                raise forms.ValidationError("The school email extension '" + ext[1].lower() + "' is not recognized")


class LoginForm(AuthenticationForm):

    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }