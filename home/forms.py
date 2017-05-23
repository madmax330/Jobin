from django.contrib.auth.models import User
from django import forms
from .models import Message, Notification


class NewUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ChangeEmailForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']


class NewMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'


class NewNotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        exclude = ('date', 'opened',)


