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
        email = clean_data.get('email')
        username = clean_data.get('username')
        if len(email) > 30:
            if not email[0:30] == username:
                raise forms.ValidationError({'username': "Username and email don't match."})
        elif not username == email:
            raise forms.ValidationError({'username': "Username and Email don't match."})
        if self.utype == 'student':
            ext = email.split('@', 1)
            ems = JobinBlockedEmail.objects.filter(extension=ext[1].lower())
            if ems.count() > 0:
                raise forms.ValidationError({'username': "The school email extension '" + ext[1].lower() + "' is not recognized"})

class ForgetFormUSer(forms.Form):
    class Meta:
        widgets = {
        'email' : forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        self.utype = kwargs.pop('utype', None)
        super(ForgetFormUSer, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super(ForgetFormUSer, self).clean()
        print("form data in clean method: %s" % cleaned_data)

class LoginForm(AuthenticationForm):

    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }