from django.db import models
from company.models import Company
from student.models import Student
from resume.models import Resume
from django.core.urlresolvers import reverse


class Post(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=0)
    title = models.CharField(max_length=100)
    wage = models.IntegerField(null=True)
    openings = models.IntegerField(null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    deadline = models.DateField()
    description = models.TextField()
    requirements = models.TextField()
    schools = models.CharField(max_length=200, null=True, default='ALL')
    programs = models.CharField(max_length=200, null=True, default='ALL')
    type = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50,  null=True)
    supplied_by_jobin = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('post:companypost', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Application(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    resume = models.ForeignKey(Resume, on_delete=models.PROTECT)
    date = models.DateField()
    status = models.CharField(max_length=25)
    cover = models.TextField(null=True, blank=True)
    post_title = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.status
