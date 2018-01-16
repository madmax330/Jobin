from django.db import models
from company.models import Company
from student.models import Student
from resume.models import Resume


class Post(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    wage = models.IntegerField(null=True, blank=True)
    wage_interval = models.CharField(max_length=20)
    openings = models.IntegerField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    deadline = models.DateField()
    responsibilities = models.TextField()
    qualifications = models.TextField()
    why_us = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    schools = models.CharField(max_length=200, null=True, default='ALL')
    programs = models.CharField(max_length=200, null=True, default='ALL')
    transcript = models.BooleanField(default=False)
    type = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50,  null=True, default='open')
    supplied_by_jobin = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    new_apps = models.BooleanField(default=False)
    cover_instructions = models.TextField(null=True, blank=True)
    is_startup_post = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    date_posted = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    resume = models.ForeignKey(Resume, on_delete=models.PROTECT)
    date = models.DateField()
    opened = models.BooleanField(default=False)
    status = models.CharField(max_length=25)
    cover = models.TextField(null=True, blank=True)
    cover_requested = models.BooleanField(default=False)
    cover_submitted = models.BooleanField(default=False)
    cover_opened = models.BooleanField(default=False)
    post_title = models.CharField(max_length=100)
    student_name = models.CharField(max_length=100)
    resume_notified = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status
