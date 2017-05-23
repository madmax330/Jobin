from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Company
from .forms import NewCompanyForm, EditCompanyForm

from post.util_post import CompanyPostContainer
from event.util_event import CompanyEventContainer

from post.classes import ExtendedApplication

from resume.util_resume import ResumeContainer


class CompanyContainer(BaseContainer):
    def __init__(self, user):
        super(CompanyContainer, self).__init__()
        self._container_name = 'Company Container'
        self.__user = user
        try:
            self.__company = Company.objects.get(user=user)
        except ObjectDoesNotExist:
            self.__company = None
        self.__post_container = CompanyPostContainer(self.__company)
        self.__event_container = CompanyEventContainer(self.__company)

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_company(self, c_info, user):
        info = {
            'user': user.id,
            'name': c_info['name'],
            'address': c_info['address'],
            'city': c_info['city'],
            'state': c_info['state'],
            'zipcode': c_info['zipcode'],
            'country': c_info['country'],
            'phone': c_info['phone'],
            'email': user.email,
            'points': 0,
            'website': c_info['website'],
            'is_startup': c_info['is_startup'],
        }
        self._form = NewCompanyForm(info)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def edit_company(self, info):
        info = {
            'name': info['name'],
            'address': info['address'],
            'city': info['city'],
            'state': info['state'],
            'zipcode': info['zipcode'],
            'country': info['country'],
            'phone': info['phone'],
            'website': info['website'],
            'is_startup': info['is_startup'],
        }
        self._form = EditCompanyForm(info, instance=self.__company)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_company(self):
        return self.__company

    def get_user(self):
        return self.__user

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    #
    #
    #   POST RELATED ACTIONS
    #
    #

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_post(self, info):
        if self.__post_container.new_post(info):
            return True
        else:
            self.add_error_list(self.__post_container.get_errors())
            return False

    def edit_post(self, pk, info):
        if self.__post_container.get_post(pk):
            if self.__post_container.edit_post(info):
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def close_post(self, pk):
        if self.__post_container.get_post(pk):
            if self.__post_container.close_post():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def recover_post(self, pk, info):
        if self.__post_container.get_post(pk):
            if self.__post_container.recover_post(info):
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_post(self, pk):
        return self.__post_container.get_post(pk)

    def get_posts(self):
        return self.__post_container.get_posts()

    def get_expired_posts(self):
        return self.__post_container.get_expired_posts()

    def get_application(self, pk):
        return self.__post_container.get_application(pk)

    def get_extended_application(self, app):
        rc = ResumeContainer(app.student)
        return ExtendedApplication(
            app,
            app.student,
            rc.get_extended_resume(app.resume)
        )

    def get_applications(self, pk, ak='0', filters=None):
        if self.get_post(pk):
            return self.__post_container.get_applications(ak=ak, filters=filters)
        else:
            self.add_error_list(self.__post_container.get_errors())
            return None

    def application_count(self, pk):
        if self.get_post(pk):
            return self.__post_container.application_count()
        self.add_error_list(self.__post_container.get_errors())
        return False

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def request_cover_letter(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.request_cover():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def close_application(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.close_application():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    #
    #
    #   EVENT RELATED ACTIONS
    #
    #

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_event(self, info):
        if self.__event_container.new_event(info):
            return True
        else:
            self.add_error_list(self.__event_container.get_errors())
            return False

    def edit_event(self, pk, info):
        if self.__event_container.get_event(pk):
            if self.__event_container.edit_event(info):
                return True
        self.add_error_list(self.__event_container.get_errors())
        return False

    def close_event(self, pk):
        if self.__event_container.get_event(pk):
            if self.__event_container.close_event():
                return True
        self.add_error_list(self.__event_container.get_errors())
        return False

    def recover_event(self, pk, info):
        if self.__event_container.get_event(pk):
            if self.__event_container.recover_event(info):
                return True
        self.add_error_list(self.__event_container.get_errors())
        return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_event(self, pk):
        return self.__event_container.get_event(pk)

    def get_events(self):
        return self.__event_container.get_events()

    def get_expired_events(self):
        return self.__event_container.get_expired_events()

    #  DATA MODIFY FUNCTIONS (UPDATERS)








