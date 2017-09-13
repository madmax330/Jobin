from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from .models import JobinProgram, JobinMajor, JobinSchool, JobinTerritory, JobinBlockedEmail, JobinRequestedEmail,JobinInvalidUser
from company.models import Company, Suggestion
from student.models import Student

from post.models import Post, Application
from event.models import Event, SavedEvent
from resume.models import Resume


class JobinAdmin(admin.AdminSite):

    def get_urls(self):
        urls = super(JobinAdmin, self).get_urls()
        plus_urls = [
            url(r'^site/statistics/$', self.site_stats_view),
        ]
        return plus_urls + urls

    def site_stats_view(self, request):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return redirect('home:index')
        users = {
            'count': User.objects.all().count(),
            'requested_emails': JobinRequestedEmail.objects.all(),
        }
        companies = {
            'count': Company.objects.count(),
            'posts': Post.objects.count(),
            'internships': Post.objects.filter(type='internship').count(),
            'volunteer': Post.objects.filter(type='volunteer').count(),
            'full_time': Post.objects.filter(type='full_time').count(),
            'part_time': Post.objects.filter(type='part_time').count(),
            'startup': Post.objects.filter(is_startup_post=True).count(),
            'events': Event.objects.count(),
        }
        students = {
            'count': Student.objects.count(),
            'applications': Application.objects.count(),
            'saved_events': SavedEvent.objects.count(),
            'resumes': Resume.objects.count(),
            'file_resumes': Resume.objects.exclude(file_resume__isnull=True).count(),
        }
        context = {
            'users': users,
            'companies': companies,
            'students': students,
        }
        return render(request, 'home/admin/index.html', context)

admin_site = JobinAdmin('Jobin Admin Site')
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
