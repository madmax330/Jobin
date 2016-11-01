from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from student.models import Student
from .models import Resume, Language, Experience, Award, School, Skill, SchoolLink, SkillLink, ExperienceLink, AwardLink, LanguageLink
from home.models import Message
from post.models import Application
from .forms import ResumeForm, LanguageForm, ExperienceForm, AwardForm, SchoolForm, SkillForm, NewResumeForm
from django.core.exceptions import ObjectDoesNotExist
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
        ll = LanguageLink.objects.filter(resume=resume)
        sl = SchoolLink.objects.filter(resume=resume)
        el = ExperienceLink.objects.filter(resume=resume).order_by('-start')
        skl = SkillLink.objects.filter(resume=resume)
        al = AwardLink.objects.filter(resume=resume)
        languages = []
        for x in ll:
            languages.append(x.language)
        schools = []
        for x in sl:
            schools.append(x.school)
        experience = []
        for x in el:
            experience.append(x.experience)
        skills = []
        for x in skl:
            skills.append(x.skill)
        awards = []
        for x in al:
            awards.append(x.award)
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
            x = Message()
            x.code = 'info'
            x.student = s
            x.message = 'Your profile was successfully created. Welcome to Jobin!'
            x.save()
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
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = resume.student
        x.save()
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
        l = LanguageLink()
        l.resume = nr
        l.language = x.language
        l.save()
    for x in schs:
        s = SchoolLink()
        s.school = x.school
        s.resume = nr
        s.save()
    for x in exps:
        e = ExperienceLink()
        e.experience = x.experience
        e.start = x.experience.start
        e.resume = nr
        e.save()
    for x in skills:
        s = SkillLink()
        s.skill = x.skill
        s.resume = nr
        s.save()
    for x in aws:
        a = AwardLink()
        a.award = x.award
        a.resume = nr
        a.save()
    m = Message()
    m.student = nr.student
    m.code = 'info'
    m.message = 'Your new resume was successfully created based on ' + cr.name + '. You can now taylor it to your needs.'
    m.save()
    return redirect('resume:index')


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm

    def form_valid(self, form):
        resume = form.save(commit=False)
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
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
        apps = Application.objects.filter(resume=resume).count()
        if apps > 0:
            resume.status = 'closed'
            resume.save()
            return redirect('resume:index')
        return self.post(*args, **kwargs)


class NewLanguageView(CreateView):
    model = Language
    form_class = LanguageForm

    def form_valid(self, form):
        language = form.save(commit=False)
        language.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        language.rkey = r.pk
        x = Message()
        x.code = 'info'
        x.message = 'Your Language record was created successfully.'
        x.student = language.student
        x.save()
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
        x = Message()
        x.code = 'info'
        x.message = 'Your language object was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
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
            m = Message()
            m.code = 'info'
            m.message = 'Your language object was deleted successfully.'
            m.student = resume.student
            m.save()
            return redirect('resume:languagelist', kwargs={'rk': resume.pk})


class NewExperienceView(CreateView):
    model = Experience
    form_class = ExperienceForm

    def form_valid(self, form):
        exp = form.save(commit=False)
        exp.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        exp.rkey = r.pk
        x = Message()
        x.code = 'info'
        x.message = 'Your Experience was recorded successfully.'
        x.student = exp.student
        x.save()
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


class DeleteExperience(DeleteView):
    model = Experience

    def get_success_url(self):
        rk = self.kwargs['rk']
        x = Message()
        x.code = 'info'
        x.message = 'Your experience object was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
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
            m = Message()
            m.code = 'info'
            m.message = 'Your experience object was deleted successfully.'
            m.student = resume.student
            m.save()
            return redirect('resume:experiencelist', kwargs={'rk': resume.pk})


class NewAwardView(CreateView):
    model = Award
    form_class = AwardForm

    def form_valid(self, form):
        aw = form.save(commit=False)
        aw.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        aw.rkey = r.pk
        x = Message()
        x.code = 'info'
        x.message = 'Your Award was recorded successfully.'
        x.student = aw.student
        x.save()
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


class DeleteAward(DeleteView):
    model = Award

    def get_success_url(self):
        rk = self.kwargs['rk']
        x = Message()
        x.code = 'info'
        x.message = 'Your award object was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
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
            m = Message()
            m.code = 'info'
            m.message = 'Your award object was deleted successfully.'
            m.student = resume.student
            m.save()
            return redirect('resume:awardlist', kwargs={'rk': resume.pk})


class NewSchoolView(CreateView):
    model = School
    form_class = SchoolForm

    def form_valid(self, form):
        school = form.save(commit=False)
        school.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        school.rkey = r.pk
        x = Message()
        x.code = 'info'
        x.message = 'Your School record was created successfully.'
        x.student = school.student
        x.save()
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


class DeleteSchool(DeleteView):
    model = School

    def get_success_url(self):
        rk = self.kwargs['rk']
        x = Message()
        x.code = 'info'
        x.message = 'Your school object was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
        return reverse_lazy('resume:schoollist', kwargs={'rk': rk})

    def get(self, *args, **kwargs):
        resume = Resume.objects.get(pk=kwargs['rk'])
        sch = School.objects.get(pk=kwargs['pk'])
        link = SchoolLink.objects.filter(resume=resume, school=sch)
        link.delete()
        links = SchoolLink.objects.filter(school=sch)
        if links.count() == 0:
            return self.post(*args, **kwargs)
        else:
            m = Message()
            m.code = 'info'
            m.message = 'Your school object was deleted successfully.'
            m.student = resume.student
            m.save()
            return redirect('resume:schoollist', kwargs={'rk': resume.pk})


class NewSkillView(CreateView):
    model = Skill
    form_class = SkillForm

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.student = Student.objects.get(user=self.request.user)
        r = Resume.objects.get(pk=self.kwargs['rk'])
        skill.rkey = r.pk
        x = Message()
        x.code = 'info'
        x.message = 'Your Skill was recorded successfully.'
        x.student = skill.student
        x.save()
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


class DeleteSkill(DeleteView):
    model = Skill

    def get_success_url(self):
        rk = self.kwargs['rk']
        x = Message()
        x.code = 'info'
        x.message = 'Your skill object was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
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
            m = Message()
            m.code = 'info'
            m.message = 'Your language object was deleted successfully.'
            m.student = resume.student
            m.save()
            return redirect('resume:skilllist', kwargs={'rk': resume.pk})


class MakeActive(View):

    def get(self, request, pk, rq):
        student = Student.objects.get(user=self.request.user)
        resumes = Resume.objects.filter(student=student)
        for x in resumes:
            x.is_active = False
            x.save()
        r = Resume.objects.get(pk=pk)
        r.is_active = True
        r.save()
        xx = Message()
        xx.code = 'info'
        xx.message = 'Resume ' + r.name + ' set to active resume.'
        xx.student = r.student
        xx.save()
        if rq == 'post':
            return redirect('post:studentposts')
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
            s.save()
            l = SchoolLink()
            l.resume = resume
            l.school = s
            l.save()
            m = Message()
            m.code = 'info'
            m.student = student
            m.message = 'Your School record was created successfully.'
            m.save()
            return redirect('resume:nav', rk=rk, rq='school_done')
        x = Message()
        x.code = 'danger'
        x.student = student
        x.message = 'Error creating your record, please try again.'
        x.save()
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
            s.save()
            l = SchoolLink()
            l.resume = resume
            l.school = s
            l.save()
            m = Message()
            m.code = 'info'
            m.student = student
            m.message = 'Your School record was created successfully.'
            m.save()
            if rq == 'new':
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='school_done')
        x = Message()
        x.code = 'danger'
        x.student = student
        x.message = 'Error creating your record, please try again.'
        x.save()
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
            l.save()
            link = LanguageLink()
            link.resume = resume
            link.language = l
            link.save()
            m = Message()
            m.code = 'info'
            m.student = student
            m.message = 'Your Language record was created successfully.'
            m.save()
            if rq == 'new':
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            return redirect('resume:nav', rk=rk, rq='language_done')
        x = Message()
        x.code = 'danger'
        x.student = student
        x.message = 'Error creating your record, please try again.'
        x.save()
        return self.get(request, rk=rk, rq='continue')


class ExperienceWalkthrough(View):
    template_name = 'resume/walkthrough_experience.html'
    form_class = ExperienceForm

    def get(self, request, rk):
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

    def post(self, request, rk):
        form = self.form_class(request.POST)
        student = Student.objects.get(user=self.request.user)
        resume = Resume.objects.get(pk=rk)

        if form.is_valid():
            e = form.save(commit=False)
            e.student = student
            e.save()
            l = ExperienceLink()
            l.resume = resume
            l.experience = e
            l.start = e.start
            l.save()
            m = Message()
            m.code = 'info'
            m.student = student
            m.message = 'Your Experience record was created successfully.'
            m.save()
            return self.get(request, rk=rk)
        x = Message()
        x.code = 'danger'
        x.student = student
        x.message = 'Error creating your record, please try again.'
        x.save()
        return self.get(request, rk=rk)


class WalkthrougNav(View):

    def get(self, request, rk, rq):
        resume = Resume.objects.get(pk=rk)
        student = resume.student
        if rq == 'resume_done':
            return redirect('resume:firstschoolwalk', rk=rk)
        if rq == 'school_done':
            sch = SchoolLink.objects.filter(resume=resume)
            if sch.count() > 0:
                return redirect('resume:languagewalk', rk=rk, rq='continue')
            else:
                x = Message()
                x.code = 'danger'
                x.student = Student.objects.get(user=self.request.user)
                x.message = "You must add at least one school entry before continuing."
                x.save()
                return redirect('resume:schoolwalk', rk=rk, rq='continue')
        if rq == 'language_done':
            langs = LanguageLink.objects.filter(resume=resume)
            if langs.count() > 0:
                return redirect('resume:experiencewalk', rk=rk)
            else:
                x = Message()
                x.code = 'danger'
                x.student = Student.objects.get(user=self.request.user)
                x.message = "You must add at least one language entry before continuing."
                x.save()
                return redirect('resume:languagewalk', rk=rk, rq='continue')
        if rq == 'experience_done':
            resume.is_complete = True
            resume.save()
            x = Message()
            x.code = 'info'
            x.student = Student.objects.get(user=self.request.user)
            x.message = 'Your resume was successfully created and is ready to be used in an application.'
            x.save()
            xx = Message()
            xx.code = 'info'
            xx.student = x.student
            xx.message = 'You can upload a file resume as well by going to edit resume.'
            xx.save()
            xxx = Message()
            xxx.code = 'info'
            xxx.student = x.student
            xxx.message = 'Fill in the rest of your resume information (Schools, Languages, Skills, Awards and Work' \
                          'Experience) with the manage button or on the overview screen.'
            xxx.save()
        return redirect('resume:index')


def linkschool(request, pk, rk):
    school = School.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    l = SchoolLink()
    l.resume = resume
    l.school = school
    l.save()
    return redirect('resume:schoollist', rk=rk)


def linkaward(request, pk, rk):
    award = Award.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    l = AwardLink()
    l.resume = resume
    l.award = award
    l.save()
    return redirect('resume:awardlist', rk=rk)


def linkexperience(request, pk, rk):
    experience = Experience.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    l = ExperienceLink()
    l.resume = resume
    l.experience = experience
    l.start = experience.start
    l.save()
    return redirect('resume:experiencelist', rk=rk)


def linklanguage(request, pk, rk):
    language = Language.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    l = LanguageLink()
    l.resume = resume
    l.language = language
    l.save()
    return redirect('resume:languagelist', rk=rk)


def linkskill(request, pk, rk):
    skill = Skill.objects.get(pk=pk)
    resume = Resume.objects.get(pk=rk)
    l = SkillLink()
    l.resume = resume
    l.skill = skill
    l.save()
    return redirect('resume:skilllist', rk=rk)
