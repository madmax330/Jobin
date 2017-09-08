from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from smtplib import SMTPException
from django.contrib.auth.models import AnonymousUser

from .base_classes import BaseContainer

from .models import JobinActivation
from .forms import NewActivationForm

import datetime
from django.utils import timezone
import hashlib


class ActivationUtil(BaseContainer):

    def __init__(self, user):
        super(ActivationUtil, self).__init__()
        self._container_name = 'Activation Util'
        self.__user = user

    def send_activation_email(self):
        if isinstance(self.__user, AnonymousUser):
            self.add_error('User not authenticated.')
            return False
        activation_key = self.__create_activation_key()
        subject = 'Jobin Account Verification'
        template = 'home/utils/email/activate_email.html'
        url = 'http://jobin.ca/activate/' + activation_key
        html = render_to_string(template, {'link': url})
        text_val = strip_tags(html)

        from_email = 'info@jobin.ca'
        msg = EmailMultiAlternatives(subject, text_val, from_email,  [self.__user.email])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send(fail_silently=False)
        except SMTPException as e:
            self.add_error('Error sending email: ' + str(e))
            return False

        if self.__new_activation(activation_key):
            return True
        return False

    def activate_user(self, key):
        activation = self.__confirm_activation_key(key)
        if activation:
            self.__user = activation.user
            if self.__user.is_active:
                self.add_error('User already verified.')
                activation.delete()
                return False
            self.__user.is_active = True
            self.__user.save()
            activation.delete()
            return True
        else:
            return False

    def send_new_password(self, password):
        subject = 'Password Reset'
        template = 'home/utils/email/new_password.html'
        html = render_to_string(template, {'password': password})
        text_val = strip_tags(html)

        from_email = 'info@jobin.ca'
        msg = EmailMultiAlternatives(subject, text_val, from_email, [self.__user.email])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send(fail_silently=False)
            return True
        except SMTPException as e:
            self.add_error('Error sending email: ' + str(e))
            return False

    def get_password(self):
        return self.__create_activation_key()[:25]

    def clear_codes(self):
        codes = JobinActivation.objects.filter(user=self.__user)
        for x in codes:
            x.delete()

    def __create_activation_key(self):
        chars = 'igvbjk,dsaf21905273+_)(*^%%%@^&*(..,,djfgh226'
        secret_key = get_random_string(20, chars)
        return hashlib.sha256((secret_key + self.__user.username).encode('utf-8')).hexdigest()

    def __confirm_activation_key(self, key):
        try:
            activation = JobinActivation.objects.get(key=key)
        except ObjectDoesNotExist:
            self.add_error('Invalid activation key.')
            return None
        if timezone.now() < activation.expiration:
            return activation

    def __new_activation(self, key):
        info = {
            'key': key,
            'user': self.__user.id,
            'expiration': datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=1), "%Y-%m-%d %H:%M:%S")
        }
        self._form = NewActivationForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        self.add_form_errors()
        return False

