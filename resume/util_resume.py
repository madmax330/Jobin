from django.core.exceptions import ObjectDoesNotExist

from home.base_classes import BaseContainer

from .models import Resume, Language, LanguageLink, School, SchoolLink, Reference, ReferenceLink
from .models import Experience, ExperienceLink, Skill, SkillLink, Award, AwardLink

from .forms import ResumeForm, NewLanguageForm, EditLanguageForm, NewLanguageLinkForm
from .forms import NewExperienceForm, EditExperienceForm, NewExperienceLinkForm
from .forms import NewAwardForm, EditAwardForm, NewAwardLinkForm
from .forms import NewSchoolForm, EditSchoolForm, NewSchoolLinkForm
from .forms import NewSkillForm, EditSkillForm, NewSkillLinkForm
from .forms import NewReferenceForm, EditReferenceForm, NewReferenceLinkForm

from .classes import ExtendedResume

import datetime


class ResumeContainer(BaseContainer):

    def __init__(self, student):
        super(ResumeContainer, self).__init__()
        self._container_name = 'Resume Container'
        self.__student = student
        self.__resume = None

    #  DATA CREATION FUNCTIONS (SETTERS)

    def new_resume(self, r_info):
        info = {
            'student': self.__student.id,
            'name': r_info['name'],
            'gpa': r_info['gpa'],
            'is_active': False,
            'last_updated': datetime.datetime.now(),
        }
        self._form = ResumeForm(info)
        if self._form.is_valid():
            new_resume = self._form.save()
            active_resume = self.get_active_resume()
            if active_resume:
                self.__resume = active_resume
                for x in self.get_schools():
                    self.__resume = new_resume
                    if not self.link_school(x):
                        return False
                self.__resume = active_resume
                for x in self.get_languages():
                    self.__resume = new_resume
                    if not self.link_language(x):
                        return False
                if self.is_complete():
                    self.mark_as_complete()
                m = 'Your education and languages have been imported from current active resume.'
                if not self.new_message(True, self.__student, m, 0):
                    return False
            self.__resume = new_resume
            return True
        else:
            self.add_form_errors()
            return False

    def copy_resume(self):
        info = {
            'student': self.__resume.student.id,
            'name': self.__resume.name + ' COPY',
            'gpa': self.__resume.gpa,
            'is_active': False,
            'last_updated': datetime.datetime.now(),
        }
        self._form = ResumeForm(info)
        if self._form.is_valid():
            r = self._form.save()
            schools = self.get_schools()
            languages = self.get_languages()
            experience = self.get_experience_list()
            awards = self.get_awards()
            skills = self.get_skills()
            references = self.get_references()
            self.__resume = r
            for x in schools:
                if not self.link_school(x):
                    return False
            for x in languages:
                if not self.link_language(x):
                    return False
            for x in experience:
                if not self.link_experience(x):
                    return False
            for x in awards:
                if not self.link_award(x):
                    return False
            for x in skills:
                if not self.link_skill(x):
                    return False
            for x in references:
                if not self.link_reference(x):
                    return False

            self.__resume.is_complete = True
            self.__resume.save()
            return True

    def edit_resume(self, r_info):
        info = {
            'student': self.__student.id,
            'name': r_info['name'],
            'gpa': r_info['gpa'],
            'last_updated': datetime.datetime.now(),
        }
        self._form = ResumeForm(info, instance=self.__resume)
        if self._form.is_valid():
            self.__resume = self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def close_resume(self, in_apps):
        for x in self.get_schools():
            if not self.delete_school_link(x):
                return False
        for x in self.get_languages():
            if not self.delete_language_link(x):
                return False
        for x in self.get_experience_list():
            if not self.delete_experience_link(x):
                return False
        for x in self.get_awards():
            if not self.delete_award_link(x):
                return False
        for x in self.get_skills():
            if not self.delete_skill_link(x):
                return False
        for x in self.get_references():
            if not self.delete_reference_link(x):
                return False
        if in_apps:
            self.__resume.status = 'closed'
            if self.__resume.is_active:
                self.__resume.is_active = False
            self.__resume.save()
            return True
        else:
            self.__resume.delete()
            return True

    def new_school(self, i_info):
        info = {
            'student': self.__student.id,
            'name': i_info['name'],
            'program': i_info['program'],
            'level': i_info['level'],
            'start': i_info['start'],
            'end': i_info['end'],
            'is_current': i_info['is_current'],
            'rkey': self.__resume.id,
            'rname': self.__resume.name,
        }
        self._form = NewSchoolForm(info)
        if self._form.is_valid():
            s = self._form.save()
            if self.link_school(s):
                if self.is_complete():
                    self.mark_as_complete()
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_school(self, s, i_info):
        info = {
            'name': i_info['name'],
            'program': i_info['program'],
            'level': i_info['level'],
            'start': i_info['start'],
            'end': i_info['end'],
            'is_current': i_info['is_current'],
        }
        self._form = EditSchoolForm(info, instance=s)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_school(self, s):
        if self.delete_school_link(s):
            if not self.is_complete():
                self.mark_as_incomplete()
            return True
        else:
            return False

    def new_language(self, i_info):
        info = {
            'student': self.__student.id,
            'name': i_info['name'],
            'level': i_info['level'],
            'rkey': self.__resume.id,
            'rname': self.__resume.name,
        }
        self._form = NewLanguageForm(info)
        if self._form.is_valid():
            l = self._form.save()
            if self.link_language(l):
                if self.is_complete():
                    self.mark_as_complete()
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_language(self, l, i_info):
        info = {
            'name': i_info['name'],
            'level': i_info['level'],
        }
        self._form = EditLanguageForm(info, instance=l)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_language(self, l):
        if self.delete_language_link(l):
            if not self.is_complete():
                self.mark_as_incomplete()
            return True
        else:
            return False

    def new_experience(self, i_info):
        info = {
            'student': self.__student.id,
            'title': i_info['title'],
            'start': i_info['start'],
            'end': i_info['end'],
            'description': i_info['description'],
            'company': i_info['company'],
            'experience_type': i_info['experience_type'],
            'is_current': i_info['is_current'],
            'rkey': self.__resume.id,
            'rname': self.__resume.name,
        }
        self._form = NewExperienceForm(info)
        if self._form.is_valid():
            e = self._form.save()
            if self.link_experience(e):
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_experience(self, e, i_info):
        info = {
            'title': i_info['title'],
            'start': i_info['start'],
            'end': i_info['end'],
            'description': i_info['description'],
            'company': i_info['company'],
            'experience_type': i_info['experience_type'],
            'is_current': i_info['is_current'],
        }
        self._form = EditExperienceForm(info, instance=e)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_experience(self, e):
        if self.delete_experience_link(e):
            return True
        else:
            return False

    def new_award(self, i_info):
        info = {
            'student': self.__student.id,
            'title': i_info['title'],
            'date': i_info['date'],
            'description': i_info['description'],
            'award_type': i_info['award_type'],
            'rkey': self.__resume.id,
            'rname': self.__resume.name,
        }
        self._form = NewAwardForm(info)
        if self._form.is_valid():
            a = self._form.save()
            if self.link_award(a):
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_award(self, a, i_info):
        info = {
            'title': i_info['title'],
            'date': i_info['date'],
            'description': i_info['description'],
            'award_type': i_info['award_type'],
        }
        self._form = EditAwardForm(info, instance=a)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_award(self, a):
        if self.delete_award_link(a):
            return True
        else:
            return False

    def new_skill(self, i_info):
        info = {
            'student': self.__student.id,
            'name': i_info['name'],
            'level': i_info['level'],
            'rkey': self.__resume.id,
            'rname': self.__resume.name,
        }
        self._form = NewSkillForm(info)
        if self._form.is_valid():
            s = self._form.save()
            if self.link_skill(s):
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_skill(self, s, i_info):
        info = {
            'name': i_info['name'],
            'level': i_info['level'],
        }
        self._form = EditSkillForm(info, instance=s)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_skill(self, s):
        if self.delete_skill_link(s):
            return True
        else:
            return False

    def new_reference(self, i_info):
        info = {
            'student': self.__student.id,
            'name': i_info['name'],
            'email': i_info['email'],
            'affiliation': i_info['affiliation']
        }
        self._form = NewReferenceForm(info)
        if self._form.is_valid():
            r = self._form.save()
            if self.link_reference(r):
                return True
            return False
        else:
            self.add_form_errors()
            return False

    def edit_reference(self, r, i_info):
        info = {
            'name': i_info['name'],
            'email': i_info['email'],
            'affiliation': i_info['affiliation']
        }
        self._form = EditReferenceForm(info, instance=r)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_reference(self, r):
        if self.delete_reference_link(r):
            return True
        else:
            return False

    def link_school(self, s):
        info = {
            'resume': self.__resume.id,
            'school': s.id,
        }
        self._form = NewSchoolLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_school_link(self, o):
        try:
            l = SchoolLink.objects.get(resume=self.__resume, school=o)
            l.delete()
            if SchoolLink.objects.filter(school=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    def link_language(self, l):
        info = {
            'resume': self.__resume.id,
            'language': l.id,
        }
        self._form = NewLanguageLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_language_link(self, o):
        try:
            l = LanguageLink.objects.get(resume=self.__resume, language=o)
            l.delete()
            if LanguageLink.objects.filter(language=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    def link_experience(self, e):
        info = {
            'resume': self.__resume.id,
            'experience': e.id,
            'start': e.start,
        }
        self._form = NewExperienceLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_experience_link(self, o):
        try:
            l = ExperienceLink.objects.get(resume=self.__resume, experience=o)
            l.delete()
            if ExperienceLink.objects.filter(experience=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    def link_award(self, a):
        info = {
            'resume': self.__resume.id,
            'award': a.id,
        }
        self._form = NewAwardLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_award_link(self, o):
        try:
            l = AwardLink.objects.get(resume=self.__resume, award=o)
            l.delete()
            if AwardLink.objects.filter(award=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    def link_skill(self, s):
        info = {
            'resume': self.__resume.id,
            'skill': s.id,
        }
        self._form = NewSkillLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_skill_link(self, o):
        try:
            l = SkillLink.objects.get(resume=self.__resume, skill=o)
            l.delete()
            if SkillLink.objects.filter(skill=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    def link_reference(self, r):
        info = {
            'resume': self.__resume.id,
            'reference': r.id,
        }
        self._form = NewReferenceLinkForm(info)
        if self._form.is_valid():
            self._form.save()
            return True
        else:
            self.add_form_errors()
            return False

    def delete_reference_link(self, o):
        try:
            l = ReferenceLink.objects.get(resume=self.__resume, reference=o)
            l.delete()
            if ReferenceLink.objects.filter(reference=o).count() == 0:
                o.delete()
            return True
        except ObjectDoesNotExist:
            self.add_error('Link not found.')
            return False

    #  DATA FETCH FUNCTIONS (GETTERS)

    def get_active_resume(self):
        try:
            return Resume.objects.get(student=self.__student, is_active=True, is_complete=True)
        except ObjectDoesNotExist:
            self.add_error('No active resume.')
            return None

    def is_first_resume(self):
        self.__resume = self.get_active_resume()
        return self.__resume is not None

    def get_resume(self, pk=None):
        if pk:
            try:
                self.__resume = Resume.objects.get(pk=pk)
                if self.__resume.student == self.__student:
                    return self.__resume
                else:
                    self.add_error('Resume not found.')
                    return None
            except ObjectDoesNotExist:
                self.add_error('Resume not found.')
                return None
        else:
            return self.__resume

    def get_extended_resume(self, resume=None):
        if resume:
            self.__resume = resume
        return ExtendedResume(resume,
                              self.get_languages(),
                              self.get_schools(),
                              self.get_experience_list(),
                              self.get_awards(),
                              self.get_skills(),
                              self.get_references())

    def get_resumes(self):
        resumes = Resume.objects.filter(student=self.__student, status='open')
        if resumes.count() > 0:
            for x in resumes:
                self.__resume = x
                self.clean_resume()
            return list(resumes)
        else:
            self.add_error('No resumes found.')
            return []

    def get_school(self, pk):
        try:
            s = School.objects.get(pk=pk)
            if s.student == self.__student:
                return s
            else:
                self.add_error('School not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('School not found.')
            return None

    def get_schools(self):
        ls = SchoolLink.objects.filter(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.school)
            return l
        else:
            self.add_error('No schools found.')
            return []

    def get_other_schools(self):
        ls = SchoolLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.school)
            return l
        else:
            self.add_error('No other schools found.')
            return []

    def get_language(self, pk):
        try:
            l = Language.objects.get(pk=pk)
            if l.student == self.__student:
                return l
            else:
                self.add_error('Language not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('Language not found.')
            return None

    def get_languages(self):
        ls = LanguageLink.objects.filter(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.language)
            return l
        else:
            self.add_error('No languages found.')
            return []

    def get_other_languages(self):
        ls = LanguageLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.language)
            return l
        else:
            self.add_error('No other languages found.')
            return []

    def get_experience(self, pk):
        try:
            e = Experience.objects.get(pk=pk)
            if e.student == self.__student:
                return e
            else:
                self.add_error('Experience not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('Experience not found.')
            return None

    def get_experience_list(self):
        ls = ExperienceLink.objects.filter(resume=self.__resume).order_by('-start')
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.experience)
            return l
        else:
            self.add_error('No experience found.')
            return []

    def get_other_experience_list(self):
        ls = ExperienceLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.experience)
            return l
        else:
            self.add_error('No other experience found.')
            return []

    def get_award(self, pk):
        try:
            a = Award.objects.get(pk=pk)
            if a.student == self.__student:
                return a
            else:
                self.add_error('Award not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('Award not found.')
            return None

    def get_awards(self):
        ls = AwardLink.objects.filter(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.award)
            return l
        else:
            self.add_error('No awards found.')
            return []

    def get_other_awards(self):
        ls = AwardLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.award)
            return l
        else:
            self.add_error('No other awards found.')
            return []

    def get_skill(self, pk):
        try:
            s = Skill.objects.get(pk=pk)
            if s.student == self.__student:
                return s
            else:
                self.add_error('Skill not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('Skill not found.')
            return None

    def get_skills(self):
        ls = SkillLink.objects.filter(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.skill)
            return l
        else:
            self.add_error('No skills found.')
            return []

    def get_other_skills(self):
        ls = SkillLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if ls.count() > 0:
            l = []
            for x in ls:
                l.append(x.skill)
            return l
        else:
            self.add_error('No other skills found.')
            return []

    def get_reference(self, pk):
        try:
            r = Reference.objects.get(pk=pk)
            if r.student == self.__student:
                return r
            else:
                self.add_error('Reference not found.')
                return None
        except ObjectDoesNotExist:
            self.add_error('Reference not found.')
            return None

    def get_references(self):
        rs = ReferenceLink.objects.filter(resume=self.__resume)
        if rs.count() > 0:
            l = []
            for x in rs:
                l.append(x.reference)
            return l
        else:
            self.add_error('No references found.')
            return []

    def get_other_references(self):
        rs = ReferenceLink.objects.filter(resume__student=self.__student).exclude(resume=self.__resume)
        if rs.count() > 0:
            l = []
            for x in rs:
                l.append(x.reference)
            return l
        else:
            self.add_error('No other references found.')
            return []

    #  DATA MODIFY FUNCTIONS (UPDATERS)

    def make_active_resume(self):
        if not self.__resume.is_complete:
            self.add_error('Cannot set incomplete resume to active resume.')
            return False
        l = Resume.objects.filter(student=self.__student)
        for x in l:
            if not x == self.__resume:
                x.is_active = False
                x.save()
        self.__resume.is_active = True
        self.__resume.save()
        return True

    def mark_as_complete(self):
        if not self.__resume.is_complete:
            self.__resume.is_complete = True
            self.__resume.save()

    def mark_as_incomplete(self):
        if self.__resume.is_complete:
            self.__resume.is_complete = False
            self.__resume.save()

    def is_complete(self):
        schools = self.get_schools()
        languages = self.get_languages()
        if not (len(schools) > 0 and len(languages) > 0):
            return False
        return True

    def clean_resume(self):
        if not self.__resume.is_complete:
            schools = self.get_schools()
            languages = self.get_languages()
            for x in schools:
                self.delete_school(x)
            for x in languages:
                self.delete_language(x)





