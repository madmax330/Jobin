from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Company, Suggestion
from .forms import NewCompanyForm, EditCompanyForm, NewSuggestionForm

from post.util_post import CompanyPostContainer
from event.util_event import CompanyEventContainer

from post.classes import ExtendedApplication, HomePagePost

from resume.util_resume import ResumeContainer

import datetime


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
            'industry': c_info['industry'],
        }
        self._form = NewCompanyForm(info)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def edit_company(self, c_info):
        info = {
            'name': c_info['name'],
            'address': c_info['address'],
            'city': c_info['city'],
            'state': c_info['state'],
            'zipcode': c_info['zipcode'],
            'country': c_info['country'],
            'phone': c_info['phone'],
            'website': c_info['website'],
            'is_startup': c_info['is_startup'],
            'industry': c_info['industry']
        }
        self._form = EditCompanyForm(info, instance=self.__company)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def new_suggestion(self, i_info):
        info = {
            'company': self.__company.id,
            'topic': i_info['topic'],
            'suggestion': i_info['suggestion'],
            'importance': i_info['importance'],
        }
        self._form = NewSuggestionForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_company(self):
        return self.__company

    def get_user(self):
        return self.__user

    def get_suggestions(self):
        l = Suggestion.objects.filter(company=self.__company)
        if l.count() > 0:
            return list(l)
        return []

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def not_new(self):
        self.__company.is_new = False
        self.__company.save()
        return True

    def comment_suggestion(self, pk, comment):
        try:
            suggestion = Suggestion.objects.get(pk=pk)
            if suggestion.comments:
                suggestion.comments = suggestion.comments + '\n' + str(datetime.datetime.now().date()) + ' - ' + comment
            else:
                suggestion.comments = str(datetime.datetime.now().date()) + ' - ' + comment
            suggestion.save()
            return True
        except ObjectDoesNotExist:
            self.add_error('Suggestion not found.')
            return False

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
            self.save_form(self.__post_container.get_form())
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

    def get_home_posts(self):
        results = []
        posts = self.__post_container.get_posts()
        for x in posts:
            results.append(HomePagePost(x, self.__post_container.application_count(x)))
        return results

    def get_application(self, pk):
        return self.__post_container.get_application(pk)

    def get_extended_application(self, app):
        self.__post_container.app_opened(app)
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

    def save_application(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.save_application():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def remove_application_save(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.remove_application_save():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

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

    def no_new_apps(self, post=None):
        self.__post_container.no_new_apps(post)

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
            self.save_form(self.__event_container.get_form())
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








