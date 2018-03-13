from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from home.models import JobinRequestedSchool
from home.forms import JobinRequestedSchoolForm

from .models import Student
from .forms import NewStudentForm, EditStudentForm, TranscriptForm

from post.util_post import StudentPostContainer, CompanyPostContainer
from resume.util_resume import ResumeContainer
from event.util_event import StudentEventContainer, CompanyEventContainer

from resume.classes import ExtendedResume

from django.utils import timezone


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

    def new_student(self, info, user):
        info['user'] = user.id
        info['name'] = info['firstname'] + ' ' + info['lastname']
        info['school'] = None
        info['email'] = user.email
        info['last_login'] = timezone.now().date()
        self._form = NewStudentForm(info)
        if self._form.is_valid():
            self.__student = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    def edit_student(self, info):
        info['name'] = info['firstname'] + ' ' + info['lastname']
        self._form = EditStudentForm(info, instance=self.__student)
        if self._form.is_valid():
            self.__student = self._form.save()
            return True
        else:
            self.save_form()
            self.add_form_errors()
            return False

    # DATA FETCH FUNCTIONS (GETTERS)

    def get_student(self):
        return self.__student

    def get_user(self):
        return self.__user

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def add_transcript(self, info, files):
        if self.delete_transcript():
            self._form = TranscriptForm(info, files, instance=self.__student)
            if self._form.is_valid():
                self._form.save()
                return True
            self.add_form_errors()
        return False

    def delete_transcript(self):
        if self.__student.transcript:
            self.__student.transcript.delete()
            self.__student.transcript = None
            self.__student.save()
        return True

    def request_school_verification(self, info):
        self.__student.school_email = info['email']
        self.__student.school = info['school']
        self.__student.save()
        return True

    def request_new_school(self, info):
        if not (info['name'] and info['country']):
            self.add_error('School name and country must be specified.')
            return False
        info['name'] = info['name'].lower()
        requests = JobinRequestedSchool.objects.filter(name=info['name'], country=info['country'])
        if requests.count():
            school = requests.first()
            school.count = school.count + 1
            school.save()
        else:
            info['count'] = 1
            self._form = JobinRequestedSchoolForm(info)
            if self._form.is_valid():
                self._form.save()
            else:
                self.add_form_errors()
                return False
        self.__student.school_requested = info['name'].lower()
        self.__student.save()
        return True

    def email_verified(self):
        return not self.__user.groups.filter(name='student_email_not_verified').exists()

    def school_verified(self):
        self.__student.verified = True
        self.__student.save()
        return True

    def change_school(self):
        self.__student.verified = False
        self.__student.school_requested = None
        self.__student.school_email = ''
        self.__student.save()
        return True

    def not_new(self):
        self.__student.is_new = False
        self.__student.save()
        return True

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

    def get_posts(self, cat, pk, filters=None):
        return self.__post_container.get_posts(cat, pk, filters)

    def get_post_count(self, category, filters=None):
        return self.__post_container.get_post_count(category, filters)

    def get_newest_posts(self):
        return self.__post_container.get_newest_posts()

    def get_application(self, pk):
        a = self.__post_container.get_application(pk)
        if a:
            return a
        else:
            self.add_form_errors(self.__post_container.get_errors())
            return None

    def get_pdf_resume_info(self, rk):
        if self.__resume_container.get_resume(rk):
            return {
                'name': self.__student.name,
                'school': self.__student.school if self.__student.school else '',
                'program': self.__student.program,
                'major': self.__student.major,
                'email': self.__student.email,
                'phone': self.__student.phone,
                'address': '%s, %s, %s, %s' % (self.__student.address, self.__student.city, self.__student.state, self.__student.zipcode),
                'resume': self.__resume_container.get_extended_resume(self.__resume_container.get_resume())
            }

    def get_applications(self):
        return self.__post_container.get_applications()

    def get_old_applications(self):
        return self.__post_container.get_old_applications()

    def get_all_applications(self):
        return self.__post_container.get_all_applications()

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def increment_view_count(self, pk):
        if self.__post_container.get_post(pk):
            if self.__post_container.increment_view_count():
                return True
        self.add_error_list(self.__post_container.get_errors())
        return False

    def change_application_resume(self, pk, ak):
        if self.__post_container.get_application(ak):
            if self.__resume_container.get_resume(pk):
                if self.__post_container.change_application_resume(self.__resume_container.get_resume()):
                    return True
                else:
                    self.add_error_list(self.__post_container.get_errors())
                    return False
            self.add_error_list(self.__resume_container.get_errors())
            return False
        else:
            self.add_error_list(self.__post_container.get_errors())
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
            self.add_error_list(self.__event_container.get_errors())
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
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_school(self, pk, ok):
        o = self.__resume_container.get_school(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_school(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
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
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_language(self, pk, ok):
        o = self.__resume_container.get_language(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_language(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
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
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_experience(self, pk, ok):
        o = self.__resume_container.get_experience(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_experience(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
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
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_award(self, pk, ok):
        o = self.__resume_container.get_award(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_award(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
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
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_skill(self, pk, ok):
        o = self.__resume_container.get_skill(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_skill(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
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

    def new_reference(self, pk, info):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.new_reference(info):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def add_reference(self, pk, ok):
        o = self.__resume_container.get_reference(ok)
        if o and self.__resume_container.get_resume(pk):
            if self.__resume_container.link_reference(o):
                for x in self.__post_container.get_resume_applications(self.__resume_container.get_resume()):
                    self.__post_container.notify_resume(x)
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def edit_reference(self, pk, info):
        o = self.__resume_container.get_reference(pk)
        if o:
            if self.__resume_container.edit_reference(o, info):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_reference(self, rk, pk):
        if self.__resume_container.get_resume(rk):
            o = self.__resume_container.get_reference(pk)
            if o:
                if self.__resume_container.delete_reference(o):
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
                self.__resume_container.get_skills(),
                self.__resume_container.get_references(),
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

    def get_references(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_references()
        return []

    def get_other_references(self, pk=None):
        if self.__resume_container.get_resume(pk):
            return self.__resume_container.get_other_references()
        return []

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def add_file_resume(self, pk, post, file):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.add_file_resume(post, file):
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

    def delete_file_resume(self, pk):
        if self.__resume_container.get_resume(pk):
            if self.__resume_container.delete_file_resume():
                return True
        self.add_error_list(self.__resume_container.get_errors())
        return False

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
