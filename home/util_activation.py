from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from smtplib import SMTPException
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import Group

from .base_classes import BaseContainer

from .models import JobinActivation, JobinSchool
from .forms import NewActivationForm

from website.settings import TIME_ZONE
import datetime, pytz
from django.utils import timezone
import hashlib


class ActivationUtil(BaseContainer):

    def __init__(self, user):
        super(ActivationUtil, self).__init__()
        self._container_name = 'Activation Util'
        self.__user = user

    def get_user(self):
        return self.__user

    def send_activation_email(self, student):
        if isinstance(self.__user, AnonymousUser):
            self.add_error('User not authenticated.')
            return False
        activation_key = self.__create_activation_key()
        if self.__new_activation(activation_key):
            subject = 'Jobin Account Verification'
            template = 'home/utils/email/activate_email.html'
            url = 'https://jobin.ca/activate/' + ('student/' if student else 'company/') + activation_key + '/'
            html = render_to_string(template, {'link': url})
            text_val = strip_tags(html)

            from_email = 'info@jobin.ca'
            msg = EmailMultiAlternatives(subject, text_val, from_email,  [self.__user.email])
            msg.attach_alternative(html, "text/html")
            try:
                msg.send(fail_silently=False)
                return True
            except SMTPException as e:
                self.add_error('Error sending email: ' + str(e))
                return False
        return False

    def activate_student(self, key):
        activation = self.__confirm_activation_key(key)
        if activation:
            self.__user = activation.user
            g = Group.objects.get(name='student_email_not_verified')
            try:
                g.user_set.remove(self.__user)
            except:
                self.add_error('User already verified.')
                return False
            return True
        else:
            return False

    def activate_company(self, key):
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
        else:
            self.add_error('Activation key expired, please get a new one.')
            return None

    def __new_activation(self, key):
        info = {
            'key': key,
            'user': self.__user.id,
            'expiration': datetime.datetime.strftime(
                datetime.datetime.now(pytz.timezone(TIME_ZONE)) + datetime.timedelta(days=1),
                "%Y-%m-%d %H:%M:%S"
            )
        }
        self._form = NewActivationForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        self.add_form_errors()
        return False


    #
    #
    #   STUDENT SCHOOL VERIFICATION FUNCTIONS
    #
    #

    def send_student_school_verification(self, info):
        if not (info['school'] and info['email']):
            self.add_error('School name and email cannot be left blank.')
            return False
        try:
            school = JobinSchool.objects.get(name=info['school'])
        except ObjectDoesNotExist:
            self.add_error('School not found.')
            return False
        arr = info['email'].split('@', 1)
        if len(arr) == 2 and school.email == arr[1]:
            activation_key = self.__create_activation_key()
            if self.__new_activation(activation_key):
                subject = 'Jobin School Email Verification'
                template = 'home/utils/email/verify_school_email.html'
                url = 'https://jobin.ca/student/verify/student/school/' + activation_key + '/'
                html = render_to_string(template, {'link': url})
                text_val = strip_tags(html)

                from_email = 'info@jobin.ca'
                msg = EmailMultiAlternatives(subject, text_val, from_email,  [info['email']])
                msg.attach_alternative(html, "text/html")
                try:
                    msg.send(fail_silently=False)
                    return True
                except SMTPException as e:
                    self.add_error('Error sending email: ' + str(e))
                    return False
            return False
        self.add_error('School email not recognized for "' + school.name + '".')
        return False

    def verify_student_school(self, key):
        activation = self.__confirm_activation_key(key)
        if activation:
            self.__user = activation.user
            activation.delete()
            return True
        else:
            return False

    #
    #   Contact Email
    #

    def send_contact_email(self, info):
        subject = 'Contact message from ' + info['email']
        template = 'home/utils/email/contact_message.html'
        html = render_to_string(template, {'info': info})
        text_val = strip_tags(html)

        from_email = 'jobin@jobin.ca'
        msg = EmailMultiAlternatives(subject, text_val, from_email, ['baba.kourouma@jobin.ca', 'maxence.coulibaly@jobin.ca'])
        msg.attach_alternative(html, "text/html")
        try:
            msg.send(fail_silently=False)
            return True
        except SMTPException as e:
            self.add_error('Error sending email: ' + str(e))
            return False





