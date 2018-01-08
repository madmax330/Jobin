from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer
from .util_activation import ActivationUtil

from .models import JobinSchool, JobinBlockedEmail, JobinRequestedEmail
from .forms import NewUserForm, ChangeEmailForm, ChangePasswordForm


class UserUtil(BaseContainer):

    def __init__(self, user):
        super(UserUtil, self).__init__()
        self._container_name = 'User Util'
        self.__user = user

    #
    #   USER LOGIN FUNCTIONS
    #

    def log_user_in(self, request, info):
        self.__user = authenticate(username=info['email'], password=info['password'])
        if self.__user is not None:
            if self.__user.is_active:
                login(request, self.__user)
                return 1
            else:
                login(request, self.__user)
                self.add_error('User not active.')
                return -1
        else:
            try:
                u = User.objects.get(email=info['email'])
                if u.check_password(info['password']):
                    return -1
            except ObjectDoesNotExist:
                self.add_error('Invalid login credentials.')
                return 0
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
            self.add_error('Passwords do not match')
            return False
        self._form = NewUserForm(info)
        if self._form.is_valid():
            self.__user = self._form.save(commit=False)
            self.__user.set_password(self._form.cleaned_data['password'])
            self.__user.save()

            if student:
                g = Group.objects.get(name='student_user')
                g.user_set.add(self.__user)
            else:
                g = Group.objects.get(name='company_user')
                g.user_set.add(self.__user)
            activation = ActivationUtil(self.__user)
            if activation.send_activation_email():
                return True
            else:
                self.add_error_list(activation.get_errors())
                return False
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

    def get_user(self):
        return self.__user

    def get_user_type(self):
        if self.__user.groups.filter(name='company_user').exists():
            return 'company'
        elif self.__user.groups.filter(name='student_user').exists():
            return 'student'
        else:
            self.add_error('No user type found.')
            return ''

    #
    #   USER CHANGE FUNCTIONS
    #

    def activate_user(self, key):
        activation = ActivationUtil(self.__user)
        if activation.activate_user(key):
            return True
        self.add_error_list(activation.get_errors())
        return False

    def new_activation_key(self, info):
        try:
            self.__user = User.objects.get(email=info['email'])
        except ObjectDoesNotExist:
            self.add_error('Invalid email.')
            return False
        if self.__user.is_active:
            self.add_error('User already activated.')
            return False
        else:
            activation = ActivationUtil(self.__user)
            activation.clear_codes()
            if activation.send_activation_email():
                return True
            self.add_error_list(activation.get_errors())
            return False

    def new_password(self, mail):
        try:
            self.__user = User.objects.get(email=mail)
        except ObjectDoesNotExist:
            self.add_error('Invalid email.')
            return False
        activation = ActivationUtil(self.__user)
        password = activation.get_password()
        self.__user.set_password(password)
        self.__user.save()
        if activation.send_new_password(password):
            return True
        self.add_error_list(activation.get_errors())
        return False






