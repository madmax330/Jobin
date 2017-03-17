from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Student

from post.util_post import StudentPostContainer


class StudentContainer(BaseContainer):

    def __init__(self, user):
        super(StudentContainer, self).__init__()
        self._container_name = 'Student Container'
        try:
            self.__student = Student.objects.get(user=user)
        except ObjectDoesNotExist:
            self.__student = None
        self.__post_container = StudentPostContainer(self.__student)

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_application(self, post, resume):
        if self.__post_container.new_application(post, resume):
            return True
        else:
            self.add_error_list(self.__post_container.get_errors())
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_student(self):
        return self.__student

    def get_application(self, pk):
        a = self.__post_container.get_application(pk)
        if a:
            return a
        else:
            self.add_form_errors(self.__post_container.get_errors())
            return None

    def get_applications(self):
        apps = self.__post_container.get_applications()
        if apps:
            return apps
        else:
            self.add_error_list(self.__post_container.get_errors())
            return None

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def add_cover_letter(self, pk, letter):
        if self.__post_container.get_application(pk):
            if self.__post_container.add_cover_letter(letter):
                return True
            else:
                self.add_error_list(self.__post_container.get_errors())
                return False
        else:
            self.add_error_list(self.__post_container.get_errors())
            return False













