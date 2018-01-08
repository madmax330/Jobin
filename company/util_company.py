from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Company, Suggestion
from .forms import NewCompanyForm, EditCompanyForm, UploadLogoForm, NewSuggestionForm

from post.util_post import CompanyPostContainer
from event.util_event import CompanyEventContainer

from post.classes import ExtendedApplication, HomePagePost

from resume.util_resume import ResumeContainer

from django.utils import timezone


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

    def new_company(self, info, user):
        info['user'] = user.id
        info['email'] = user.email
        info['points'] = 0
        self._form = NewCompanyForm(info)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def edit_company(self, info):
        self._form = EditCompanyForm(info, instance=self.__company)
        if self._form.is_valid():
            self.__company = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def new_suggestion(self, info):
        info['company'] = self.__company.id
        self._form = NewSuggestionForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.save_form()
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

    def upload_logo(self, post, file):
        if self.delete_logo():
            self._form = UploadLogoForm(post, file, instance=self.__company)
            if self._form.is_valid():
                self._form.save()
                return True
            self.add_form_errors()
        return False

    def delete_logo(self):
        if self.__company.logo:
            self.__company.logo.delete()
        return True

    def comment_suggestion(self, pk, info):
        try:
            suggestion = Suggestion.objects.get(pk=pk)
            if not info['comment']:
                self.add_error('Comment cannot be left blank.')
                return False
            if suggestion.comments:
                suggestion.comments = suggestion.comments + '\n' + str(timezone.now().date()) + ' - ' + info['comment']
            else:
                suggestion.comments = str(timezone.now().date()) + ' - ' + info['comment']
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
            else:
                self.save_form(self.__post_container.get_form())
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
        post = self.__post_container.get_post(pk)
        if post:
            if post.notified:
                post.notified = False
                post.save()
            return post
        return None

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
        app = self.__post_container.get_application(pk)
        self.__post_container.remove_application_resume_notified()
        return app

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
            else:
                self.save_form(self.__event_container.get_form())
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








