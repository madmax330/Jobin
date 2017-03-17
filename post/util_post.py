from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Application
from .forms import NewApplicationForm, AddCoverLetterForm

import datetime


class StudentPostContainer(BaseContainer):

    def __init__(self, student):
        super(StudentPostContainer, self).__init__()
        self._container_name = 'Student Post Container'
        self.__student = student
        self.__post = None
        self.__application = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_application(self, post, resume, ):
        info = {
            'student': self.__student.id,
            'post': post.id,
            'resume': resume.id,
            'date': datetime.datetime.now().date(),
            'post_title': post.title,
            'student_name': self.__student.firstname + ' ' + self.__student.lastname
        }
        self._form = NewApplicationForm(info)
        if self._form.is_valid():
            self.__application = self._form.save()
            m = 'Application for post ' + post.title + ' successful.'
            if self.new_message(True, self.__student, m, 0):
                return True
            else:
                return False
        else:
            self.add_form_errors()
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    def get_application(self, pk):
        try:
            self.__application = Application.objects.get(pk=pk)
            return self.__application
        except ObjectDoesNotExist:
            self.add_error('Application not found.')
            return None

    def get_applications(self):
        apps = Application.objects.filter(student=self.__student, status='active')
        if apps.count() > 0:
            return list(apps)
        self.add_error('No applications found.')
        return None

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def add_cover_letter(self, letter):
        info = {
            'cover': letter,
            'cover_submitted': True,
        }
        self._form = AddCoverLetterForm(info, instance=self.__application)
        if self._form.is_valid():
            self.__application = self._form.save()
            m = 'Cover letter for "' + self.__application.post_title + '" successfully submitted.'
            if self.new_message(True, self.__student, m, 0):
                return True
            else:
                return False
        else:
            self.add_form_errors()
            return False


class CompanyPostContainer(BaseContainer):

    def __init__(self):
        super(CompanyPostContainer, self).__init__()



