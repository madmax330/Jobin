from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from home.models import Message
from home.utils import new_message
from post.models import Application
from .forms import ResumeForm, LanguageForm, ExperienceForm, AwardForm, SchoolForm, SkillForm, NewResumeForm
from django.core.exceptions import ObjectDoesNotExist
from .utils import *
import datetime


class IndexView(View):
    template_name = 'resume/resume_list.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            msgs = Message.objects.filter(student=student)
            context = {
                'list': Resume.objects.filter(student=student, status='open'),
                'msgs': msgs
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
        languages = get_languages(resume)
        schools = get_schools(resume)
        experience = get_experience(resume)
        skills = get_skills(resume)
        awards = get_awards(resume)
        context = {
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
            msg = 'Your profile was successfully created. Welcome to Jobin!'
            new_message('student', s, 'info', msg)
            s.is_new = False
            s.save()
        msgs = Message.objects.filter(student=s)
        rs = Resume.objects.filter(student=s)
        context['msgs'] = msgs
        context['rs'] = rs
        context['rcount'] = rs.count()
        for x in msgs:
            x.delete()
        return context

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.student = Student.objects.get(user=self.request.user)
        msg = 'Your resume was created successfully.'
        new_message('student', resume.student, 'info', msg)
        s = resume.student
        if s.is_new:
            s.is_new = False
            s.save()
        if resume.is_active:
            rs = Resume.objects.filter(student=s)
            for r in rs:
                r.is_active = False
                r.save()
        return super(NewResumeView, self).form_valid(form)


def copyresume(request, rk):
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
        create_language_link(x.language, nr)
    for x in schs:
        create_school_link(x.school, nr)
    for x in exps:
        create_experience_link(x.experience, nr)
    for x in skills:
        create_skill_link(x.skill, nr)
    for x in aws:
        create_award_link(x.award, nr)
    msg = 'Your new resume was successfully created based on ' + cr.name + '. You can now taylor it to your needs.'
    new_message('student', nr.student, 'info', msg)
    return redirect('resume:index')


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm

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


class DeleteResume(DeleteView):
    model = Resume
    success_url = reverse_lazy('resume:index')

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['pk'])
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
        msg = 'Your resume was deleted successfully.'
        new_message('student', resume.student, 'info', msg)
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
        items = get_other_language(resume)
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
        msg = 'Your Language record was created successfully.'
        new_message('student', language.student, 'info', msg)
        update_resume(r)
        return super(NewLanguageView, self).form_valid(form)


class LanguageList(View):
    template_name = 'resume/language_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        ll = LanguageLink.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
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


class DeleteLanguage(DeleteView):
    model = Language

    def get_success_url(self):
        rk = self.kwargs['rk']
        msg = 'Your language object was deleted successfully.'
        new_message('student', Student.objects.get(user=self.request.user), 'info', msg)
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
            msg = 'Your language object was deleted successfully.'
            new_message('student', resume.student, 'info', msg)
            return redirect('resume:languagelist', rk=resume.pk)


class NewExperienceView(CreateView):
    model = Experience
    form_class = ExperienceForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewExperienceView, self).get_context_data(**kwargs)
        items = get_other_experience(resume)
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
        msg = 'Your Experience was recorded successfully.'
        new_message('student', exp.student, 'info', msg)
        update_resume(r)
        return super(NewExperienceView, self).form_valid(form)


class ExperienceList(View):
    template_name = 'resume/experience_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        el = ExperienceLink.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
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
        msg = 'Your Experience was successfully updated.'
        new_message('student', x.student, 'info', msg)
        return super(ExperienceUpdateView, self).form_valid(form)


class DeleteExperience(DeleteView):
    model = Experience

    def get_success_url(self):
        rk = self.kwargs['rk']
        msg = 'Your experience object was deleted successfully.'
        new_message('student', Student.objects.get(user=self.request.user), 'info', msg)
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
            msg = 'Your experience object was deleted successfully.'
            new_message('student', resume.student, 'info', msg)
            return redirect('resume:experiencelist', rk=resume.pk)


class NewAwardView(CreateView):
    model = Award
    form_class = AwardForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewAwardView, self).get_context_data(**kwargs)
        items = get_other_award(resume)
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
        msg = 'Your Award was recorded successfully.'
        new_message('student', aw.student, 'info', msg)
        update_resume(r)
        return super(NewAwardView, self).form_valid(form)


class AwardList(View):
    template_name = 'resume/award_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        al = AwardLink.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
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
        msg = 'Your Award was successfully updated.'
        new_message('student', x.student, 'info', msg)
        return super(AwardUpdateView, self).form_valid(form)


class DeleteAward(DeleteView):
    model = Award

    def get_success_url(self):
        rk = self.kwargs['rk']
        msg = 'Your award object was deleted successfully.'
        new_message('student', Student.objects.get(user=self.request.user), 'info', msg)
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
            msg = 'Your award object was deleted successfully.'
            new_message('student', resume.student, 'info', msg)
            return redirect('resume:awardlist', rk=resume.pk)


class NewSchoolView(CreateView):
    model = School
    form_class = SchoolForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewSchoolView, self).get_context_data(**kwargs)
        items = get_other_school(resume)
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
        msg = 'Your School record was created successfully.'
        new_message('student', school.student, 'info', msg)
        update_resume(r)
        return super(NewSchoolView, self).form_valid(form)


class SchoolList(View):
    template_name = 'resume/school_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        sl = SchoolLink.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
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
        msg = 'Your School was successfully updated.'
        new_message('student', x.student, 'info', msg)
        return super(SchoolUpdateView, self).form_valid(form)


class DeleteSchool(DeleteView):
    model = School

    def get_success_url(self):
        rk = self.kwargs['rk']
        msg = 'Your school object was deleted successfully.'
        new_message('student', Student.objects.get(user=self.request.user), 'info', msg)
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
            msg = 'Your school object was deleted successfully.'
            new_message('student', resume.student, 'info', msg)
            return redirect('resume:schoollist', rk=resume.pk)


class NewSkillView(CreateView):
    model = Skill
    form_class = SkillForm

    def get_context_data(self, **kwargs):
        resume = Resume.objects.get(pk=self.kwargs['rk'])
        context = super(NewSkillView, self).get_context_data(**kwargs)
        items = get_other_skill(resume)
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
        msg = 'Your Skill was recorded successfully.'
        new_message('student', skill.student, 'info', msg)
        update_resume(r)
        return super(NewSkillView, self).form_valid(form)


class SkillList(View):
    template_name = 'resume/skill_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        sl = SkillLink.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
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
        msg = 'Your Skill was successfully updated.'
        new_message('student', x.student, 'info', msg)
        return super(SkillUpdateView, self).form_valid(form)


class DeleteSkill(DeleteView):
    model = Skill

    def get_success_url(self):
        rk = self.kwargs['rk']
        msg = 'Your skill object was deleted successfully.'
        new_message('student', Student.objects.get(user=self.request.user), 'info', msg)
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
            msg = 'Your language object was deleted successfully.'
            new_message('student', resume.student, 'info', msg)
            return redirect('resume:skilllist', rk=resume.pk)


class MakeActive(View):

    def get(self, request, pk, rq):
        r = Resume.objects.get(pk=pk)
        make_active(r.student, r)
        msg = 'Resume ' + r.name + ' set to active resume.'
        new_message('student', r.student, 'info', msg)
        if rq == 'post':
            return redirect('post:studentposts', pk=0, pt='internship')
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
        msgs = Message.objects.filter(student=student)
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
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
            create_school_link(s, resume)
            msg = 'Your School record was created successfully.'
            new_message('student', student, 'info', msg)
            return redirect('resume:nav', rk=rk, rq='school_done')
        msg = 'Error creating your record, please try again.'
        new_message('student', student, 'danger', msg)
        return self.get(request, rk=rk)


class SchoolWalkthrough(View):
    template_name = 'resume/walkthrough_schools.html'
    form_class = SchoolForm

    def get(self, request, rk, rq):
        form = self.form_class(None)
        msgs = Message.objects.filter(student=Student.objects.get(user=self.request.user))
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
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
            create_school_link(s, resume)
            msg = 'Your School record was created successfully.'
            new_message('student', student, 'info', msg)
            if rq == 'new':
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='school_done')
        msg = 'Error creating your record, please try again.'
        new_message('student', student, 'danger', msg)
        return self.get(request, rk=rk, rq='continue')


class LanguageWalkthrough(View):
    template_name = 'resume/walkthrough_languages.html'
    form_class = LanguageForm

    def get(self, request, rk, rq):
        form = self.form_class(None)
        msgs = Message.objects.filter(student=Student.objects.get(user=self.request.user))
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
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
            create_language_link(l, resume)
            msg = 'Your Language record was created successfully.'
            new_message('student', student, 'info', msg)
            if rq == 'new':
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='language_done')
        msg = 'Error creating your record, please try again.'
        new_message('student', student, 'danger', msg)
        return self.get(request, rk=rk, rq='continue')


class ExperienceWalkthrough(View):
    template_name = 'resume/walkthrough_experience.html'
    form_class = ExperienceForm

    def get(self, request, rk, rq, pk):
        resume = Resume.objects.get(pk=rk)
        if rq == 'link':
            create_experience_link(Experience.objects.get(pk=pk), resume)
        form = self.form_class(None)
        msgs = Message.objects.filter(student=Student.objects.get(user=self.request.user))
        items = get_other_experience(resume)
        context = {
            'form': form,
            'rkey': rk,
            'msgs': msgs,
            'items': items,
            'rcount': len(items),
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
            create_experience_link(e, resume)
            msg = 'Your Experience record was created successfully.'
            new_message('student', student, 'info', msg)
            return self.get(request, rk=rk, rq=rq, pk=pk)
        msg = 'Error creating your record, please try again.'
        new_message('student', student, 'danger', msg)
        return self.get(request, rk=rk, rq=rq, pk=pk)


class WalkthrougNav(View):

    def get(self, request, rk, rq):
        resume = Resume.objects.get(pk=rk)
        student = resume.student
        if rq == 'resume_done':
            rs = Resume.objects.filter(student=student)
            if rs.count() > 1:
                ss = get_schools(rs.first())
                for s in ss:
                    create_school_link(s, resume)
                ls = get_languages(rs.first())
                for l in ls:
                    create_language_link(l, resume)
                msg = 'Since this is not your first resume, your School and Language records were brought in' \
                      ' automatically from your first resume.'
                new_message('student', student, 'warning', msg)
                return redirect('resume:experiencewalk', rk=rk, rq='default', pk='0')
            return redirect('resume:firstschoolwalk', rk=rk)
        if rq == 'school_done':
            sch = SchoolLink.objects.filter(resume=resume)
            if sch.count() > 0:
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            else:
                msg = "You must add at least one school entry before continuing."
                new_message('student', Student.objects.get(user=self.request.user), 'danger', msg)
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
        if rq == 'language_done':
            langs = LanguageLink.objects.filter(resume=resume)
            if langs.count() > 0:
                return redirect('resume:experiencewalk', rk=rk, rq='default', pk=0)
            else:
                msg = "You must add at least one language entry before continuing."
                new_message('student', Student.objects.get(user=self.request.user), 'danger', msg)
                return redirect('resume:languagewalk', rk=rk, rq='continue')
        if rq == 'experience_done':
            resume.is_complete = True
            resume.save()
            student = Student.objects.get(user=self.request.user)
            msg = 'Your resume was successfully created and is ready to be used in an application.'
            new_message('student', student, 'info', msg)
            msg = 'You can upload a file resume as well by going to edit resume.'
            new_message('student', student, 'info', msg)
            msg = 'Fill in the rest of your resume information (Schools, Languages, Skills, Awards and Work' \
                          'Experience) with the manage button or on the overview screen.'
            new_message('student', student, 'info', msg)
        return redirect('resume:index')


def linkschool(request, pk, rk):
    school = School.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if SchoolLink.objects.filter(school=school, resume=resume).count() == 0:
        create_school_link(school, resume)
    return redirect('resume:schoollist', rk=rk)


def linkaward(request, pk, rk):
    award = Award.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if AwardLink.objects.filter(award=award, resume=resume).count() == 0:
        create_award_link(award, resume)
    return redirect('resume:awardlist', rk=rk)


def linkexperience(request, pk, rk):
    experience = Experience.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if ExperienceLink.objects.filter(experience=experience, resume=resume).count() == 0:
        create_experience_link(experience, resume)
    return redirect('resume:experiencelist', rk=rk)


def linklanguage(request, pk, rk):
    language = Language.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if LanguageLink.objects.filter(language=language, resume=resume).count() == 0:
        create_language_link(language, resume)
    return redirect('resume:languagelist', rk=rk)


def linkskill(request, pk, rk):
    skill = Skill.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    if SkillLink.objects.filter(skill=skill, resume=resume).count() == 0:
        create_skill_link(skill, resume)
    return redirect('resume:skilllist', rk=rk)
