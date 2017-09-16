from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User, Group

from .models import JobinProgram, JobinMajor, JobinSchool, JobinTerritory, JobinBlockedEmail, JobinRequestedEmail, \
    JobinInvalidUser
from company.models import Company, Suggestion
from student.models import Student

from post.models import Post, Application
from event.models import Event, SavedEvent
from resume.models import Resume, Language, Experience, Award, School, Skill, Reference


class JobinAdmin(admin.AdminSite):
    def get_urls(self):
        urls = super(JobinAdmin, self).get_urls()
        plus_urls = [
            url(r'^site/statistics/$', self.site_stats_view),
            url(r'^clear/data/$', self.clear_data),
        ]
        return plus_urls + urls

    def clear_data(self, request):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return redirect('home:index')
        for x in Language.objects.all():
            x.delete()
        for x in Experience.objects.all():
            x.delete()
        for x in Skill.objects.all():
            x.delete()
        for x in School.objects.all():
            x.delete()
        for x in Award.objects.all():
            x.delete()
        for x in Reference.objects.all():
            x.delete()
        for x in Resume.objects.all():
            x.delete()
        for x in Application.objects.all():
            x.delete()
        for x in SavedEvent.objects.all():
            x.delete()
        for x in Student.objects.all():
            x.delete()
        for x in Event.objects.all():
            x.delete()
        for x in Post.objects.all():
            x.delete()
        for x in Company.objects.all():
            x.delete()
        for x in User.objects.all():
            if not x.username == 'dj@dminuser':
                x.delete()
        return HttpResponse('Data clear successful', status=200)

    def site_stats_view(self, request):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return redirect('home:index')

        users = {
            'count': User.objects.all().count(),
            'requested_emails': JobinRequestedEmail.objects.all(),
        }
        companies = {
            'count': User.objects.filter(groups__name='company_user').count(),
            'count_active': Company.objects.count(),
            'posts': Post.objects.count(),
            'internships': Post.objects.filter(type='internship').count(),
            'volunteer': Post.objects.filter(type='volunteer').count(),
            'full_time': Post.objects.filter(type='full_time').count(),
            'part_time': Post.objects.filter(type='part_time').count(),
            'startup': Post.objects.filter(is_startup_post=True).count(),
            'events': Event.objects.count(),
        }
        students = {
            'count': User.objects.filter(groups__name='student_user').count(),
            'count_active': Student.objects.count(),
            'applications': Application.objects.count(),
            'saved_events': SavedEvent.objects.count(),
            'resumes': Resume.objects.count(),
            'file_resumes': Resume.objects.filter(file_resume__isnull=False).count(),
        }

        context = {
            'users': users,
            'companies': companies,
            'students': students,
        }
        return render(request, 'home/admin/index.html', context)


admin_site = JobinAdmin('Jobin Admin Site')
admin_site.register(User)
admin_site.register(Group)
admin_site.register(JobinMajor)
admin_site.register(JobinSchool)
admin_site.register(JobinProgram)
admin_site.register(JobinTerritory)
admin_site.register(JobinBlockedEmail)
admin_site.register(JobinRequestedEmail)
admin_site.register(JobinInvalidUser)
admin_site.register(Company)
admin_site.register(Student)
admin_site.register(Suggestion)
