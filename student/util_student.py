from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from home.models import JobinSchool

from .models import Student
from .forms import NewStudentForm, EditStudentForm

from post.util_post import StudentPostContainer, CompanyPostContainer
from resume.util_resume import ResumeContainer
from event.util_event import StudentEventContainer, CompanyEventContainer

from resume.classes import ExtendedResume


class StudentContainer(BaseContainer):

    def __init__(self, user):
        super(StudentContainer, self).__init__()
        self._container_name = 'Student Container'
        self.__user = user
        try:
            self.__student = Student.objects.get(user=user)
        except ObjectDoesNotExist:
            self.__student = None
        self.__post_container = StudentPostContainer(self.__student)
        self.__resume_container = ResumeContainer(self.__student)
        self.__event_container = StudentEventContainer(self.__student)

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_student(self, s_info, user):
        ext = user.email.split('@', 1)
        s = JobinSchool.objects.filter(email=ext[1].lower())
        if not s.count() > 0:
            self.add_error('School not found.')
            return False
        info = {
            'user': user.id,
            'name': s_info['firstname'] + ' ' + s_info['lastname'],
            'firstname': s_info['firstname'],
            'lastname': s_info['lastname'],
            'dob': s_info['dob'],
            'address': s_info['address'],
            'city': s_info['city'],
            'state': s_info['state'],
            'zipcode': s_info['zipcode'],
            'country': s_info['country'],
            'school': s.first().name,
            'program': s_info['program'],
            'major': s_info['major'],
            'graduate': s_info['graduate'],
            'email': user.email,
            'phone': s_info['phone'],
            'linkedin': s_info['linkedin'],
            'work_eligible': s_info['work_eligible'],
        }
        self._form = NewStudentForm(info)
        if self._form.is_valid():
            self.__student = self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def edit_student(self, s_info):
        info = {
            'name': s_info['firstname'] + ' ' + s_info['lastname'],
            'firstname': s_info['firstname'],
            'lastname': s_info['lastname'],
            'dob': s_info['dob'],
            'address': s_info['address'],
            'city': s_info['city'],
            'state': s_info['state'],
            'zipcode': s_info['zipcode'],
            'country': s_info['country'],
            'program': s_info['program'],
            'major': s_info['major'],
            'graduate': s_info['graduate'],
            'email': s_info['email'],
            'phone': s_info['phone'],
            'linkedin': s_info['linkedin'],
            'work_eligible': s_info['work_eligible'],
        }
        self._form = EditStudentForm(info, instance=self.__student)
        if self._form.is_valid():
            self.__student = self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_student(self):
        return self.__student

    def get_user(self):
        return self.__user

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    #
    #
    #   POST RELATED ACTIONS
    #
    #

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_application(self, pk):
        p = CompanyPostContainer.fetch_post(pk)
        r = self.__resume_container.get_active_resume()
        if not p:
            self.add_error('Post not found.')
            return False
        if not r:
            self.add_error('You need an active resume to apply for posts.')
            return False
        if self.__post_container.new_application(p, r):
            return True
        else:
            self.add_error_list(self.__post_container.get_errors())
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_post(self, pk):
        return self.__post_container.get_post(pk)

    def get_posts(self, cat, pk):
        return self.__post_container.get_posts(cat, pk)

    def get_internship_count(self):
        return self.__post_container.get_internship_count()

    def get_volunteer_count(self):
        return self.__post_container.get_volunteer_count()

    def get_part_time_count(self):
        return self.__post_container.get_part_time_count()

    def get_new_grad_count(self):
        return self.__post_container.get_new_grad_count()

    def get_startup_count(self):
        return self.__post_container.get_startup_count()

    def get_application(self, pk):
        a = self.__post_container.get_application(pk)
        if a:
            return a
        else:
            self.add_form_errors(self.__post_container.get_errors())
            return None

    def get_applications(self):
        return self.__post_container.get_applications()

    def get_old_applications(self):
        return self.__post_container.get_old_applications()

    def get_all_applications(self):
        return self.__post_container.get_all_applications()

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def change_application_resume(self, pk, ak):
        if self.__post_container.get_application(ak):
            if self.__post_container.change_application_resume(self.__resume_container.get_resume(pk)):
                return True
        self.add_error_list(self.__post_container.get_errors())
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def submit_cover_letter(self, pk, letter):
        if self.__post_container.get_application(pk):
            if self.__post_container.submit_cover_letter(letter):
                return True
            else:
                self.add_error_list(self.__post_container.get_errors())
                return False
        else:
            self.add_error_list(self.__post_container.get_errors())
            return False

    def withdraw_application(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.withdraw_application():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def activate_application(self, pk):
        if self.__post_container.get_application(pk):
            if self.__post_container.activate_application():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    #
    #
    #   EVENT RELATED ACTIONS
    #
    #

    #  DATA CREATION FUNCTIONS (SETTERS)

    def save_event(self, pk):
        e = CompanyEventContainer.fetch_event(pk)
        if not e:
            self.add_error('Event not found.')
        if self.__event_container.save_event(e):
            return True
        else:
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_events(self, pk):
        return self.__event_container.get_events(pk)

    def get_saved_events(self):
        return self.__event_container.get_saved_events()

    def get_all_saved_events(self):
        return self.__event_container.get_all_saved_events()

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def remove_saved_event(self, pk):
        if self.__event_container.remove_saved_event(pk):
            return True
        self.add_error_list(self.__event_container.get_errors())
        return False

    #
    #
    #   RESUME RELATED ACTIONS
    #
    #

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_resume(self, info):
        if self.__resume_container.new_resume(info):
            return True
        else:
            self.add_error_list(self.__resume_container.get_errors())

    def edit_resume(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.edit_resume(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_resume(self, pk):
        r = self.__resume_container.get_resume(pk)
        if r:
            if self.__resume_container.close_resume(self.__post_container.in_apps(r)):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def new_school(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_school(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_school(self, pk, ok):
        o = self.__resume_container.get_school(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_school(o):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_school(self, pk, info):
        o = self.__resume_container.get_school(pk)
        if o:
            if self.__resume_container.edit_school(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_school(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_school(pk)
            if o:
                if self.__resume_container.delete_school(o):
                    return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def new_language(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_language(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_language(self, pk, ok):
        o = self.__resume_container.get_language(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_language(o):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_language(self, pk, info):
        o = self.__resume_container.get_language(pk)
        if o:
            if self.__resume_container.edit_language(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_language(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_language(pk)
            if o:
                if self.__resume_container.delete_language(o):
                    return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def new_experience(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_experience(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_experience(self, pk, ok):
        o = self.__resume_container.get_experience(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_experience(o):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_experience(self, pk, info):
        o = self.__resume_container.get_experience(pk)
        if o:
            if self.__resume_container.edit_experience(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_experience(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_experience(pk)
            if o:
                if self.__resume_container.delete_experience(o):
                    return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def new_award(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_award(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_award(self, pk, ok):
        o = self.__resume_container.get_award(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_award(o):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_award(self, pk, info):
        o = self.__resume_container.get_award(pk)
        if o:
            if self.__resume_container.edit_award(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_award(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_award(pk)
            if o:
                if self.__resume_container.delete_award(o):
                    return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def new_skill(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_skill(info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_skill(self, pk, ok):
        o = self.__resume_container.get_skill(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_skill(o):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_skill(self, pk, info):
        o = self.__resume_container.get_skill(pk)
        if o:
            if self.__resume_container.edit_skill(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_skill(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_skill(pk)
            if o:
                if self.__resume_container.delete_skill(o):
                    return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_display_resume(self, pk):
        if self.__resume_container.get_resume(pk):
            if not self.__resume_container.is_complete():
                self.add_error('Resume incomplete.')
                return None
            return ExtendedResume(
                self.__resume_container.get_resume(),
                self.__resume_container.get_languages(),
                self.__resume_container.get_schools(),
                self.__resume_container.get_experience_list(),
                self.__resume_container.get_awards(),
                self.__resume_container.get_skills()
            )
        self.add_error_list(self.__resume_container.get_errors())
        return None

    def get_resume(self, pk=None):
        return self.__resume_container.get_resume(pk)

    def get_resumes(self):
        return self.__resume_container.get_resumes()

    def get_schools(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_schools()
        return []

    def get_other_schools(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_schools()
        return []

    def get_languages(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_languages()
        return []

    def get_other_languages(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_languages()
        return []

    def get_experience(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_experience_list()
        return []

    def get_other_experience(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_experience_list()
        return []

    def get_awards(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_awards()
        return []

    def get_other_awards(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_awards()
        return []

    def get_skills(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_skills()
        return []

    def get_other_skills(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_skills()
        return []

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def copy_resume(self, pk):
        if self.get_resume(pk):
            if self.__resume_container.copy_resume():
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def make_active_resume(self, pk):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.make_active_resume():
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False
