from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from student.models import Student
from .models import Resume, Language, Experience, Award, School, Skill
from home.models import Message
from .forms import ResumeForm, LanguageForm, ExperienceForm, AwardForm, SchoolForm, SkillForm
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    template_name = 'resume/resume_list.html'

    def get(self, request):
        try:
            student = Student.objects.get(user=self.request.user)
            msgs = Message.objects.filter(student=student)
            return render(request, self.template_name, {'list': Resume.objects.filter(student=student), 'msgs': msgs})
        except ObjectDoesNotExist:
            return redirect('student:new')


class ResumeDetailView(View):
    template_name = 'resume/resume_details.html'

    def get(self, request, pk):
        resume = Resume.objects.get(pk=pk)
        languages = Language.objects.filter(resume=resume)
        schools = School.objects.filter(resume=resume)
        experience = Experience.objects.filter(resume=resume).order_by('-start')
        skills = Skill.objects.filter(resume=resume)
        awards = Award.objects.filter(resume=resume)
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
    model = Resume
    form_class = ResumeForm

    def form_valid(self, form):
        resume = form.save(commit=False)
        resume.student = Student.objects.filter(user=self.request.user).first()
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = resume.student
        x.save()
        return super(NewResumeView, self).form_valid(form)


class ResumeUpdateView(UpdateView):
    model = Resume
    form_class = ResumeForm


class DeleteResume(DeleteView):
    model = Resume
    success_url = reverse_lazy('resume:index')

    def get(self, *args, **kwargs):
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was deleted successfully.'
        x.student = Student.objects.get(user=self.request.user)
        x.save()
        return self.post(*args, **kwargs)


class NewLanguageView(CreateView):
    model = Language
    form_class = LanguageForm

    def form_valid(self, form):
        language = form.save(commit=False)
        language.resume = Resume.objects.get(pk=self.kwargs['rk'])
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = language.resume.student
        x.save()
        return super(NewLanguageView, self).form_valid(form)


class LanguageList(View):
    template_name = 'resume/language_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        languages = Language.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
        return render(request, self.template_name, {'list': languages, 'rkey': resume.pk, 'msgs': msgs})


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


class NewExperienceView(CreateView):
    model = Experience
    form_class = ExperienceForm

    def form_valid(self, form):
        exp = form.save(commit=False)
        exp.resume = Resume.objects.get(pk=self.kwargs['rk'])
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = exp.resume.student
        x.save()
        return super(NewExperienceView, self).form_valid(form)


class ExperienceList(View):
    template_name = 'resume/experience_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        experience = Experience.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
        return render(request, self.template_name, {'list': experience, 'rkey': resume.pk, 'msgs': msgs})


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


class NewAwardView(CreateView):
    model = Award
    form_class = AwardForm

    def form_valid(self, form):
        aw = form.save(commit=False)
        aw.resume = Resume.objects.get(pk=self.kwargs['rk'])
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = aw.resume.student
        x.save()
        return super(NewAwardView, self).form_valid(form)


class AwardList(View):
    template_name = 'resume/award_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        awards = Award.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
        return render(request, self.template_name, {'list': awards, 'rkey': resume.pk, 'msgs': msgs})


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


class NewSchoolView(CreateView):
    model = School
    form_class = SchoolForm

    def form_valid(self, form):
        school = form.save(commit=False)
        school.resume = Resume.objects.get(pk=self.kwargs['rk'])
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = school.resume.student
        x.save()
        return super(NewSchoolView, self).form_valid(form)


class SchoolList(View):
    template_name = 'resume/school_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        schools = School.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
        return render(request, self.template_name, {'list': schools, 'rkey': resume.pk, 'msgs': msgs})


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


class NewSkillView(CreateView):
    model = Skill
    form_class = SkillForm

    def form_valid(self, form):
        skill = form.save(commit=False)
        skill.resume = Resume.objects.get(pk=self.kwargs['rk'])
        x = Message()
        x.code = 'info'
        x.message = 'Your resume was created successfully.'
        x.student = skill.resume.student
        x.save()
        return super(NewSkillView, self).form_valid(form)


class SkillList(View):
    template_name = 'resume/skill_list.html'

    def get(self, request, rk):
        resume = Resume.objects.get(pk=rk)
        skills = Skill.objects.filter(resume=resume)
        msgs = Message.objects.filter(student=resume.student)
        return render(request, self.template_name, {'list': skills, 'rkey': resume.pk, 'msgs': msgs})


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


class MakeActive(View):

    def get(self, request, pk):
        student = Student.objects.get(user=self.request.user)
        resumes = Resume.objects.filter(student=student)
        for x in resumes:
            x.is_active = False
            x.save()
        r = Resume.objects.get(pk=pk)
        r.is_active = True
        r.save()
        return redirect('post:studentposts')
