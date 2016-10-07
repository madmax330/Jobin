from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import JobinSchool


class NewUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }

    def clean(self):
        clean_data = super(NewUserForm, self).clean()
        if not clean_data.get("username") == clean_data.get("email"):
            raise forms.ValidationError("Username and Email don't match")
        email = clean_data.get("email")
        ext = email.split('@', 1)
        school = JobinSchool.objects.filter(email=ext[1].lower())
        if not school.count() == 1:
            raise forms.ValidationError("The service is not yet open for this school." + ext[1].lower())


class LoginForm(AuthenticationForm):

    class Meta:
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        }


class InfoForm(forms.Form):
    email = forms.TextInput()
    cemail = forms.TextInput()
    password = forms.TextInput()
    cpassword = forms.TextInput()

    class Meta:
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'New Email', 'class': 'w3-input'}),
            'cemail': forms.TextInput(attrs={'placeholder': 'Confirm New Email', 'class': 'w3-input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'w3-input'}),
            'cpassword': forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'w3-input'}),
        }
        labels = {
            'email': 'Email',
            'cemail': 'Confirm Email',
            'password': 'Password',
            'cpassword': 'Confirm Password',
        }

    def clean(self):
        clean_data = super(InfoForm, self).clean()
        email = clean_data.get('email')
        password = clean_data.get('password')
        if email:
            if not email == clean_data.get('cemail'):
                raise forms.ValidationError('The emails you entered do not match')
        if password:
            if not password == clean_data.get('cpassword'):
                raise forms.ValidationError('The passwords you entered do not match')


class StudentInfoForm(InfoForm):

    class Meta:
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'New Email', 'class': 'w3-input'}),
            'cemail': forms.TextInput(attrs={'placeholder': 'Confirm New Email', 'class': 'w3-input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'w3-input'}),
            'cpassword': forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'w3-input'}),
        }
        labels = {
            'email': 'Email',
            'cemail': 'Confirm Email',
            'password': 'Password',
            'cpassword': 'Confirm Password',
        }


class CompanyInfoForm(InfoForm):

    class Meta:
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'New Email', 'class': 'form-control'}),
            'cemail': forms.TextInput(attrs={'placeholder': 'Confirm New Email', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'}),
            'cpassword': forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'}),
        }
        labels = {
            'email': 'Email',
            'cemail': 'Confirm Email',
            'password': 'Password',
            'cpassword': 'Confirm Password',
        }
