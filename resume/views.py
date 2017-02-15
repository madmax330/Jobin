from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from home.utils import MessageCenter
from post.models import Application
from .models import *
from .forms import ResumeForm, LanguageForm, ExperienceForm, AwardForm, SchoolForm, SkillForm, NewResumeForm
from django.core.exceptions import ObjectDoesNotExist
from .utils import ResumeUtil
import datetime


class IndexView(View):
    template_name = 'resume/resume_list.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            msgs = MessageCenter.get_messages('student', student)
            notes = MessageCenter.get_notifications('student', student)
            l = Resume.objects.filter(student=student, status='open')
            for x in l:
                if SchoolLink.objects.filter(resume=x).count() == 0 or LanguageLink.objects.filter(resume=x).count() == 0:
                    x.is_complete = False
                    x.save()
            if len(student.email) > 30:
                student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
            context = {
                'nav_student': student,
                'notifications': notes,
                'list': l,
                'msgs': msgs,
            }
            for x in msgs:
                x.delete()
            return render(request, self.template_name, context)
        except ObjectDoesNotExist:
            return redirect('student:new')


class ResumeDetailView(View):
    template_name = 'resume/resume_details.html'

    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk)
        languages = ResumeUtil.get_languages(resume)
        schools = ResumeUtil.get_schools(resume)
        experience = ResumeUtil.get_experience(resume)
        skills = ResumeUtil.get_skills(resume)
        awards = ResumeUtil.get_awards(resume)
        student = resume.student
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'nav_student': student,
            'resume': resume,
            'languages': languages,
            'schools': schools,
            'experience': experience,
            'skills': skills,
            'awards': awards,
        }
        return render(request, self.template_name, context)


class NewResumeView(CreateView):
    template_name = 'resume/walkthrough_resume.html'
    model = Resume
    form_class = NewResumeForm

    def get_context_data(self, **kwargs):
        context = super(NewResumeView, self).get_context_data(**kwargs)
        s = Student.objects.get(user=self.request.user)
        if s.is_new:
            MessageCenter.student_created(s)
            s.is_new = False
            s.save()
        msgs = MessageCenter.get_messages('student', s)
        rs = Resume.objects.filter(student=s)
        if len(s.email) > 30:
            s.email = s.email[0:5] + '...@' + s.email.split('@', 1)[1]
        context['msgs'] = msgs
        context['rs'] = rs
        context['rcount'] = rs.count()
        context['nav_student'] = s
        for x in msgs:
            x.delete()
        return context

    def form_valid(self, form):
        student = Student.objects.get(user=self.request.user)
        resume = form.save(commit=False)
        resume.student = student
        MessageCenter.resume_object_created(student, 'Resume', resume.name)
        if student.is_new:
            student.is_new = False
            student.save()
        if resume.is_active:
            rs = Resume.objects.filter(student=student)
            for r in rs:
                r.is_active = False
                r.save()
        return super(NewResumeView, self).form_valid(form)


def copyresume(request, rk):

    if request.method == 'GET':
        cr = Resume.objects.get(pk=rk)
        nr = Resume()
        nr.name = cr.name + ' COPY'
        nr.gpa = cr.gpa
        nr.student = cr.student
        nr.is_complete = cr.is_complete
        nr.save()
        langs = LanguageLink.objects.filter(resume=cr)
        schs = SchoolLink.objects.filter(resume=cr)
        exps = ExperienceLink.objects.filter(resume=cr)
        skills = SkillLink.objects.filter(resume=cr)
        aws = AwardLink.objects.filter(resume=cr)
        for x in langs:
            ResumeUtil.create_language_link(x.language, nr)
        for x in schs:
            ResumeUtil.create_school_link(x.school, nr)
        for x in exps:
            ResumeUtil.create_experience_link(x.experience, nr)
        for x in skills:
            ResumeUtil.create_skill_link(x.skill, nr)
        for x in aws:
            ResumeUtil.create_award_link(x.award, nr)
        MessageCenter.resume_copied(nr.student, cr.name)
        return redirect('resume:index')
    return redirect('home:index')


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm

    def get_context_data(self, **kwargs):
        context = super(ResumeUpdateView, self).get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        context['nav_student'] = student
        return context

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.last_updated = datetime.datetime.now()
        s = resume.student
        if resume.is_active:
            rs = Resume.objects.filter(student=s)
            for r in rs:
                r.is_active = False
                r.save()
        return super(ResumeUpdateView, self).form_valid(form)


def change_resume(request, rk, ak):

    if request.method == 'GET':
        app = Application.objects.get(pk=ak)
        resume = Resume.objects.get(pk=rk)
        if app.resume == resume:
            MessageCenter.resume_app_resume_already_on_file(app.student, resume.name)
        else:
            app.resume = resume
            app.resume_notified = True
            app.save()
            MessageCenter.resume_app_resume_changed(app.student, app.post_title, resume.name)
        return redirect('student:index')
    return redirect('home:index')


class DeleteResume(DeleteView):
    model = Resume
    success_url = reverse_lazy('resume:index')

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['pk'])
        if Application.objects.filter(resume=resume, status='active').count() > 0:
            MessageCenter.resume_used_in_active_applications_error(resume.student)
            return redirect('resume:index')
        ll = LanguageLink.objects.filter(resume=resume)
        sl = SchoolLink.objects.filter(resume=resume)
        el = ExperienceLink.objects.filter(resume=resume)
        al = AwardLink.objects.filter(resume=resume)
        kl = SkillLink.objects.filter(resume=resume)
        for x in ll:
            t = Language.objects.get(pk=x.language.pk)
            x.delete()
            c = LanguageLink.objects.filter(language=t).count()
            if c == 0:
                t.delete()
        for x in sl:
            t = School.objects.get(pk=x.school.pk)
            x.delete()
            c = SchoolLink.objects.filter(school=t).count()
            if c == 0:
                t.delete()
        for x in el:
            t = Experience.objects.get(pk=x.experience.pk)
            x.delete()
            c = ExperienceLink.objects.filter(experience=t).count()
            if c == 0:
                t.delete()
        for x in al:
            t = Award.objects.get(pk=x.award.pk)
            x.delete()
            c = AwardLink.objects.filter(award=t).count()
            if c == 0:
                t.delete()
        for x in kl:
            t = Skill.objects.get(pk=x.skill.pk)
            x.delete()
            c = SkillLink.objects.filter(skill=t).count()
            if c == 0:
                t.delete()
        MessageCenter.resume_object_deleted(resume.student, 'Resume', resume.name)
        apps = Application.objects.filter(resume=resume).count()
        if apps > 0:
            resume.status = 'closed'
            resume.save()
            return redirect('resume:index')
        return self.post(*args, **kwargs)


class NewLanguageView(CreateView):
    model = Language
    form_class = LanguageForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewLanguageView, self).get_context_data(**kwargs)
        items = ResumeUtil.get_other_language(resume)
        context['items'] = items
        context['icount'] = len(items)
        context['rkey'] = resume.pk
        return context

    def form_valid(self, form):
        language = form.save(commit=False)
        language.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        language.rkey = r.pk
        language.rname = r.name
        ResumeUtil.update_resume(r)
        return super(NewLanguageView, self).form_valid(form)


class LanguageList(View):
    template_name = 'resume/language_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        ll = LanguageLink.objects.filter(resume=resume)
        msgs = MessageCenter.get_messages('student', resume.student)
        languages = []
        for x in ll:
            languages.append(x.language)
        context = {
            'list': languages,
            'count': len(languages),
            'msgs': msgs,
            'rkey': rk
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class LanguageUpdateView(UpdateView):
    model = Language
    form_class = LanguageForm

    def form_valid(self, form):
        x = form.save(commit=False)
        MessageCenter.resume_object_updated(x.student, 'Language', x.name)
        return super(LanguageUpdateView, self).form_valid(form)


class DeleteLanguage(DeleteView):
    model = Language

    def get_success_url(self):
        rk = self.kwargs['rk']
        student = Student.objects.get(user=self.request.user)
        MessageCenter.resume_object_deleted(student, 'Language', None)
        return reverse_lazy('resume:languagelist', kwargs={'rk': rk})

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        lang = Language.objects.get(pk=kwargs['pk'])
        link = LanguageLink.objects.filter(resume=resume, language=lang)
        link.delete()
        links = LanguageLink.objects.filter(language=lang)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            MessageCenter.resume_object_deleted(resume.student, 'Language', lang.name)
            return redirect('resume:languagelist', rk=resume.pk)


class NewExperienceView(CreateView):
    model = Experience
    form_class = ExperienceForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewExperienceView, self).get_context_data(**kwargs)
        items = ResumeUtil.get_other_experience(resume)
        context['items'] = items
        context['icount'] = len(items)
        context['rkey'] = resume.pk
        return context

    def form_valid(self, form):
        exp = form.save(commit=False)
        exp.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        exp.rkey = r.pk
        exp.rname = r.name
        ResumeUtil.update_resume(r)
        return super(NewExperienceView, self).form_valid(form)


class ExperienceList(View):
    template_name = 'resume/experience_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        el = ExperienceLink.objects.filter(resume=resume)
        msgs = MessageCenter.get_messages('student', resume.student)
        experience = []
        for x in el:
            experience.append(x.experience)
        context = {
            'list': experience,
            'count': len(experience),
            'rkey': resume.pk,
            'msgs': msgs
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class ExperienceUpdateView(UpdateView):
    model = Experience
    form_class = ExperienceForm

    def form_valid(self, form):
        x = form.save(commit=False)
        MessageCenter.resume_object_updated(x.student, 'Experience', x.title)
        return super(ExperienceUpdateView, self).form_valid(form)


class DeleteExperience(DeleteView):
    model = Experience

    def get_success_url(self):
        rk = self.kwargs['rk']
        student = Student.objects.get(user=self.request.user)
        MessageCenter.resume_object_deleted(student, 'Experience', None)
        return reverse_lazy('resume:experiencelist', kwargs={'rk': rk})

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        exp = Experience.objects.get(pk=kwargs['pk'])
        link = ExperienceLink.objects.filter(resume=resume, experience=exp)
        link.delete()
        links = ExperienceLink.objects.filter(experience=exp)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            MessageCenter.resume_object_deleted(resume.student, 'Experience', exp.title)
            return redirect('resume:experiencelist', rk=resume.pk)


class NewAwardView(CreateView):
    model = Award
    form_class = AwardForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewAwardView, self).get_context_data(**kwargs)
        items = ResumeUtil.get_other_award(resume)
        context['items'] = items
        context['icount'] = len(items)
        context['rkey'] = resume.pk
        return context

    def form_valid(self, form):
        aw = form.save(commit=False)
        aw.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        aw.rkey = r.pk
        aw.rname = r.name
        ResumeUtil.update_resume(r)
        return super(NewAwardView, self).form_valid(form)


class AwardList(View):
    template_name = 'resume/award_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        al = AwardLink.objects.filter(resume=resume)
        msgs = MessageCenter.get_messages('student', resume.student)
        awards = []
        for x in al:
            awards.append(x.award)
        context = {
            'list': awards,
            'count': len(awards),
            'rkey': resume.pk,
            'msgs': msgs
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class AwardUpdateView(UpdateView):
    model = Award
    form_class = AwardForm

    def form_valid(self, form):
        x = form.save(commit=False)
        MessageCenter.resume_object_updated(x.student, 'Award', x.title)
        return super(AwardUpdateView, self).form_valid(form)


class DeleteAward(DeleteView):
    model = Award

    def get_success_url(self):
        rk = self.kwargs['rk']
        student = Student.objects.get(user=self.request.user)
        MessageCenter.resume_object_deleted(student, 'Award', None)
        return reverse_lazy('resume:awardlist', kwargs={'rk': rk})

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        aw = Award.objects.get(pk=kwargs['pk'])
        link = AwardLink.objects.filter(resume=resume, award=aw)
        link.delete()
        links = AwardLink.objects.filter(award=aw)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            MessageCenter.resume_object_deleted(resume.student, 'Award', aw.title)
            return redirect('resume:awardlist', rk=resume.pk)


class NewSchoolView(CreateView):
    model = School
    form_class = SchoolForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewSchoolView, self).get_context_data(**kwargs)
        items = ResumeUtil.get_other_school(resume)
        context['items'] = items
        context['icount'] = len(items)
        context['rkey'] = resume.pk
        return context

    def form_valid(self, form):
        school = form.save(commit=False)
        school.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        school.rkey = r.pk
        school.rname = r.name
        ResumeUtil.update_resume(r)
        return super(NewSchoolView, self).form_valid(form)


class SchoolList(View):
    template_name = 'resume/school_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        sl = SchoolLink.objects.filter(resume=resume)
        msgs = MessageCenter.get_messages('student', resume.student)
        schools = []
        for x in sl:
            schools.append(x.school)
        context = {
            'list': schools,
            'count': len(schools),
            'rkey': resume.pk,
            'msgs': msgs
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class SchoolUpdateView(UpdateView):
    model = School
    form_class = SchoolForm

    def form_valid(self, form):
        x = form.save(commit=False)
        MessageCenter.resume_object_updated(x.student, 'School', x.name)
        return super(SchoolUpdateView, self).form_valid(form)


class DeleteSchool(DeleteView):
    model = School

    def get_success_url(self):
        rk = self.kwargs['rk']
        student = Student.objects.get(user=self.request.user)
        MessageCenter.resume_object_deleted(student, 'School', None)
        return reverse_lazy('resume:schoollist', rk=rk)

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        sch = School.objects.get(pk=kwargs['pk'])
        link = SchoolLink.objects.filter(resume=resume, school=sch)
        link.delete()
        links = SchoolLink.objects.filter(school=sch)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            MessageCenter.resume_object_deleted(resume.student, 'School', sch.name)
            return redirect('resume:schoollist', rk=resume.pk)


class NewSkillView(CreateView):
    model = Skill
    form_class = SkillForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewSkillView, self).get_context_data(**kwargs)
        items = ResumeUtil.get_other_skill(resume)
        context['items'] = items
        context['icount'] = len(items)
        context['rkey'] = resume.pk
        return context

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        skill.rkey = r.pk
        skill.rname = r.name
        ResumeUtil.update_resume(r)
        return super(NewSkillView, self).form_valid(form)


class SkillList(View):
    template_name = 'resume/skill_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        sl = SkillLink.objects.filter(resume=resume)
        msgs = MessageCenter.get_messages('student', resume.student)
        skills = []
        for x in sl:
            skills.append(x.skill)
        context = {
            'list': skills,
            'count': len(skills),
            'rkey': resume.pk,
            'msgs': msgs
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)


class SkillUpdateView(UpdateView):
    model = Skill
    form_class = SkillForm

    def form_valid(self, form):
        x = form.save(commit=False)
        MessageCenter.resume_object_updated(x.student, 'Skill', x.name)
        return super(SkillUpdateView, self).form_valid(form)


class DeleteSkill(DeleteView):
    model = Skill

    def get_success_url(self):
        rk = self.kwargs['rk']
        student = Student.objects.get(user=self.request.user)
        MessageCenter.resume_object_deleted(student, 'Skill', None)
        return reverse_lazy('resume:skilllist', kwargs={'rk': rk})

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        skill = Skill.objects.get(pk=kwargs['pk'])
        link = SkillLink.objects.filter(resume=resume, skill=skill)
        link.delete()
        links = SkillLink.objects.filter(skill=skill)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            MessageCenter.resume_object_deleted(resume.student, 'Skill', skill.name)
            return redirect('resume:skilllist', rk=resume.pk)


class MakeActive(View):

    def get(self, request, pk, rq, fk, pt):
        r = Resume.objects.get(pk=pk)
        ResumeUtil.make_active(r.student, r)
        MessageCenter.resume_activated(r.student, r.name)
        if rq == 'post':
            return redirect('post:studentposts', pk=fk, pt=pt)
        else:
            return redirect('resume:index')


# Walkthrough Views
class FirstSchoolWalkthrough(View):
    template_name = 'resume/walkthrough_schools.html'
    form_class = SchoolForm

    def get(self, request, rk):
        student = Student.objects.get(user=self.request.user)
        sch = School()
        sch.name = student.school
        sch.program = student.program
        form = self.form_class(instance=sch)
        msgs = MessageCenter.get_messages('student', student)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
            'nav_student': student,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, rk):
        form = self.form_class(request.POST)
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)
        if form.is_valid():
            s = form.save(commit=False)
            s.student = student
            s.rkey = resume.pk
            s.rname = resume.name
            s.save()
            ResumeUtil.create_school_link(s, resume)
            MessageCenter.resume_object_created(student, 'School', s.name)
            return redirect('resume:nav', rk=rk, rq='school_done')
        MessageCenter.resume_error_creating_record(student)
        return self.get(request, rk=rk)


class SchoolWalkthrough(View):
    template_name = 'resume/walkthrough_schools.html'
    form_class = SchoolForm

    def get(self, request, rk, rq):
        student = Student.objects.get(user=self.request.user)
        res = Resume.objects.get(pk=rk)
        form = self.form_class(None)
        msgs = MessageCenter.get_messages('student', student)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
            'nav_student': res.student,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, rk, rq):
        form = self.form_class(request.POST)
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)
        if form.is_valid():
            s = form.save(commit=False)
            s.student = student
            s.rkey = resume.pk
            s.rname = resume.name
            s.save()
            ResumeUtil.create_school_link(s, resume)
            MessageCenter.resume_object_created(student, 'School', s.name)
            if rq == 'new':
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='school_done')
        MessageCenter.resume_error_creating_record(student)
        return self.get(request, rk=rk, rq='continue')


class LanguageWalkthrough(View):
    template_name = 'resume/walkthrough_languages.html'
    form_class = LanguageForm

    def get(self, request, rk, rq):
        student = Student.objects.get(user=self.request.user)
        res = Resume.objects.get(pk=rk)
        form = self.form_class(None)
        msgs = MessageCenter.get_messages('student', student)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
            'nav_student': res.student,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, rk, rq):
        form = self.form_class(request.POST)
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)

        if form.is_valid():
            l = form.save(commit=False)
            l.student = student
            l.rkey = resume.pk
            l.rname = resume.name
            l.save()
            ResumeUtil.create_language_link(l, resume)
            MessageCenter.resume_object_created(student, 'Language', l.name)
            if rq == 'new':
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='language_done')
        MessageCenter.resume_error_creating_record(student)
        return self.get(request, rk=rk, rq='continue')


class ExperienceWalkthrough(View):
    template_name = 'resume/walkthrough_experience.html'
    form_class = ExperienceForm

    def get(self, request, rk, rq, pk):
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)
        if rq == 'link':
            ResumeUtil.create_experience_link(Experience.objects.get(pk=pk), resume)
        form = self.form_class(None)
        msgs = MessageCenter.get_messages('student', student)
        items = ResumeUtil.get_other_experience(resume)
        if len(student.email) > 30:
            student.email = student.email[0:5] + '...@' + student.email.split('@', 1)[1]
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
            'items': items,
            'rcount': len(items),
            'nav_student': resume.student,
        }
        for x in msgs:
            x.delete()
        return render(request, self.template_name, context)

    def post(self, request, rk, rq, pk):
        form = self.form_class(request.POST)
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)

        if form.is_valid():
            e = form.save(commit=False)
            e.student = student
            e.rkey = resume.pk
            e.rname = resume.name
            e.save()
            ResumeUtil.create_experience_link(e, resume)
            MessageCenter.resume_object_created(student, 'Experience', e.title)
            if rq == 'continue':
                return redirect('resume:nav', rk=rk, rq='experience_done')
            return self.get(request, rk=rk, rq=rq, pk=pk)
        MessageCenter.resume_error_creating_record(student)
        return self.get(request, rk=rk, rq=rq, pk=pk)


class WalkthrougNav(View):

    def get(self, request, rk, rq):
        resume = Resume.objects.get(pk=rk)
        student = resume.student
        if rq == 'resume_done':
            rs = Resume.objects.filter(student=student)
            if rs.count() > 1:
                for x in rs:
                    if x.is_complete:
                        ss = ResumeUtil.get_schools(rs.first())
                        for s in ss:
                            ResumeUtil.create_school_link(s, resume)
                        ls = ResumeUtil.get_languages(rs.first())
                        for l in ls:
                            ResumeUtil.create_language_link(l, resume)
                        MessageCenter.resume_items_auto_copied(student)
                        return redirect('resume:experiencewalk', rk=rk, rq='default', pk='0')
            return redirect('resume:firstschoolwalk', rk=rk)
        if rq == 'school_done':
            sch = SchoolLink.objects.filter(resume=resume)
            if sch.count() > 0:
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            else:
                MessageCenter.resume_no_school(student)
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
        if rq == 'language_done':
            langs = LanguageLink.objects.filter(resume=resume)
            if langs.count() > 0:
                return redirect('resume:experiencewalk', rk=rk, rq='default', pk=0)
            else:
                MessageCenter.resume_no_language(student)
                return redirect('resume:languagewalk', rk=rk, rq='continue')
        if rq == 'experience_done':
            resume.is_complete = True
            resume.save()
            MessageCenter.resume_walkthrough_completion_message(student)
        return redirect('resume:index')


def linkschool(request, pk, rk):
    school = School.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if SchoolLink.objects.filter(school=school, resume=resume).count() == 0:
        ResumeUtil.create_school_link(school, resume)
    MessageCenter.resume_object_created(resume.student, 'School', school.name)
    return redirect('resume:schoollist', rk=rk)


def linkaward(request, pk, rk):
    award = Award.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if AwardLink.objects.filter(award=award, resume=resume).count() == 0:
        ResumeUtil.create_award_link(award, resume)
        MessageCenter.resume_object_created(resume.student, 'Award', award.title)
    return redirect('resume:awardlist', rk=rk)


def linkexperience(request, pk, rk):
    experience = Experience.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if ExperienceLink.objects.filter(experience=experience, resume=resume).count() == 0:
        ResumeUtil.create_experience_link(experience, resume)
        MessageCenter.resume_object_created(resume.student, 'Experience', experience.title)
    return redirect('resume:experiencelist', rk=rk)


def linklanguage(request, pk, rk):
    language = Language.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if LanguageLink.objects.filter(language=language, resume=resume).count() == 0:
        ResumeUtil.create_language_link(language, resume)
        MessageCenter.resume_object_created(resume.student, 'Language', language.name)
    return redirect('resume:languagelist', rk=rk)


def linkskill(request, pk, rk):
    skill = Skill.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if SkillLink.objects.filter(skill=skill, resume=resume).count() == 0:
        ResumeUtil.create_skill_link(skill, resume)
        MessageCenter.resume_object_created(resume.student, 'Skill', skill.name)
    return redirect('resume:skilllist', rk=rk)
