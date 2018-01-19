from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer
from .util_activation import ActivationUtil

from .models import JobinSchool, JobinBlockedEmail, JobinRequestedEmail
from .forms import NewUserForm, ChangeEmailForm, ChangePasswordForm

from website.settings import TIME_ZONE
import datetime, pytz
from django.utils import timezone


class UserUtil(BaseContainer):

    def __init__(self, user):
        super(UserUtil, self).__init__()
        self._container_name = 'User Util'
        self.__user = user

    #
    #   USER LOGIN FUNCTIONS
    #

    def log_user_in(self, request, info):
        u = self.get_user(email=info['email'])
        if not u:
            self.add_error('Invalid login credentials.')
            return 0
        self.__user = authenticate(username=info['email'], password=info['password'])
        if self.__user is not None:
            if self.check_student_verification():
                if self.__user.is_active:
                    login(request, self.__user)
                    return 1
            self.add_error('User account email not verified.')
            return -1
        else:
            if u.check_password(info['password']):
                return -1
            self.add_error('Invalid login credentials.')
            return 0

    def log_user_out(self, request):
        logout(request)
        return True

    def is_logged_in(self):
        return self.__user.is_authenticated()

    #
    #   USER CREATION FUNCTIONS
    #

    def new_user(self, info, student):
        if not info['password'] == info['confirm_password']:
            self.add_error('Passwords do not match.')
            return False
        if student:
            flag = self.__new_student_user(info)
        else:
            flag = self.__new_company_user(info)
        if flag:
            activation = ActivationUtil(self.__user)
            if activation.send_activation_email():
                return True
            self.add_error_list(activation.get_errors())
            return False
        return False

    def __new_student_user(self, info):
        if self.__create_user(info, True):
            g = Group.objects.get(name='student_user')
            g.user_set.add(self.__user)
            g = Group.objects.get(name='student_email_not_verified')
            g.user_set.add(self.__user)
            return True
        else:
            return False

    def __new_company_user(self, info):
        if self.__create_user(info, False):
            g = Group.objects.get(name='company_user')
            g.user_set.add(self.__user)
            return True
        else:
            return False

    def __create_user(self, info, active):
        self._form = NewUserForm(info)
        if self._form.is_valid():
            self.__user = self._form.save(commit=False)
            self.__user.is_active = active
            self.__user.set_password(self._form.cleaned_data['password'])
            self.__user.save()
            return True
        else:
            self.add_form_errors()
            return False

    def change_user_email(self, info, student=None, company=None):
        self._form = ChangeEmailForm({'username': info['email'], 'email': info['email']}, instance=self.__user)
        if self._form.is_valid():
            if student:
                self.__user = self._form.save(commit=False)
                self.__user.is_active = False
                self.__user.save()
                return True
            elif company:
                company.email = info['email']
                company.save()
                self.__user = self._form.save(commit=False)
                self.__user.is_active = False
                self.__user.save()
                activation = ActivationUtil(self.__user)
                if activation.send_activation_email():
                    return True
                else:
                    self.add_error_list(activation.get_errors())
                    return False
            else:
                self.add_error('Invalid request.')
                return False
        else:
            self.add_form_errors()
            return False

    def change_user_password(self, info):
        self._form = ChangePasswordForm({'password': info['password']}, instance=self.__user)
        if self._form.is_valid():
            self.__user = self._form.save(commit=False)
            self.__user.set_password(self._form.cleaned_data['password'])
            self.__user.save()
            return True
        else:
            self.add_form_errors()
            return False

    #
    #   USER GETTER FUNCTIONS
    #

    def get_user(self, email=None):
        if email:
            try:
                self.__user = User.objects.get(email=email)
                return self.__user
            except ObjectDoesNotExist:
                self.add_error('User not found.')
                return None
        return self.__user

    def get_user_type(self):
        if self.__user.groups.filter(name='company_user').exists():
            return 'company'
        elif self.__user.groups.filter(name='student_user').exists():
            return 'student'
        else:
            self.add_error('No user type found.')
            return ''

    def check_student_verification(self):

        zone = pytz.timezone(TIME_ZONE)
        d = datetime.datetime.strftime(
            datetime.datetime.now(zone) + datetime.timedelta(days=7),
            "%Y-%m-%d %H:%M:%S"
        )

        if zone.localize(datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")) < timezone.now() and \
                self.__user.groups.filter(name='student_email_not_verified').exists():
            return False
        return True

    #
    #   USER CHANGE FUNCTIONS
    #

    def activate_user(self, key):
        activation = ActivationUtil(self.__user)
        if self.get_user_type() == 'student':
            if activation.activate_student(key):
                return True
        else:
            if activation.activate_company(key):
                return True
        self.add_error_list(activation.get_errors())
        return False

    def new_activation_key(self, info):
        if self.get_user(email=info['email']):
            if self.__user.is_active:
                self.add_error('User already activated.')
                return False
            activation = ActivationUtil(self.__user)
            activation.clear_codes()
            if activation.send_activation_email():
                return True
            self.add_error_list(activation.get_errors())
            return False
        else:
            return False

    def new_password(self, mail):
        if self.get_user(email=mail):
            activation = ActivationUtil(self.__user)
            password = activation.get_password()
            self.__user.set_password(password)
            self.__user.save()
            if activation.send_new_password(password):
                return True
            self.add_error_list(activation.get_errors())
            return False
        else:
            return False






