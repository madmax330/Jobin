from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from home.base_classes import BaseContainer

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
                return True
            else:
                self.add_error('User not active.')
                return False
        else:
            self.add_error('Invalid login credentials.')
            return False

    def log_user_out(self, request):
        logout(request)
        return True

    def is_logged_in(self):
        return self.__user.is_authenticated()

    #
    #   USER CREATION FUNCTIONS
    #

    def new_user(self, info, student):
        self._form = NewUserForm(info)
        if self._form.is_valid():
            ext = info['email'].split('@', 1)[1].lower()
            if student:
                if JobinBlockedEmail.objects.filter(extension=ext).count() > 0:
                    self.add_error("The school email extension '" + ext + "' is not recognized.")
                    return False
            self.__user = self._form.save(commit=False)
            self.__user.set_password(self._form.cleaned_data['password'])
            self.__user.save()

            if student:
                g = Group.objects.get(name='student_user')
                g.user_set.add(self.__user)
                if JobinSchool.objects.filter(email=ext).count() == 0:
                    x = JobinRequestedEmail()
                    x.extension = ext
                    x.save()
            else:
                g = Group.objects.get(name='company_user')
                g.user_set.add(self.__user)
            return True
        else:
            self.add_form_errors()
            return False

    def change_user_email(self, info, student=None, company=None):
        self._form = ChangeEmailForm({'username': info['email'], 'email': info['email']}, instance=self.__user)
        if self._form.is_valid():
            ext = info['email'].split('@', 1)[1].lower()
            if student:
                if JobinBlockedEmail.objects.filter(extension=ext).count() > 0:
                    self.add_error("This email extension '" + ext + "' is not recognized.")
                    return False
                schools = JobinSchool.objects.filter(email=ext)
                if schools.count() == 0:
                    x = JobinRequestedEmail()
                    x.extension = ext
                    x.save()
                else:
                    student.school = schools.first().name
                    student.email = info['email']
                    student.save()
                self._form.save()
                return True
            elif company:
                company.email = info['email']
                company.save()
                self._form.save()
                return True
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
        elif self.__user.groups.filter(name='invalid_user').exists():
            return 'inactive'
        else:
            self.add_error('No user type found.')
            return ''









