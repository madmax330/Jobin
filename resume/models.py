from django.db import models
from student.models import Student
import django.utils.timezone
from django.core.urlresolvers import reverse


class Resume(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=django.utils.timezone.now)
    file_resume = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    gpa = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)

    def get_absolute_url(self):
        return reverse('resume:index')

    def __str__(self):
        return self.name


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('resume:languagelist', kwargs={'rk': self.resume.pk})

    def __str__(self):
        return self.name


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()
    description = models.TextField()
    company = models.CharField(max_length=100, null=True)
    experience_type = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('resume:experiencelist', kwargs={'rk': self.resume.pk})

    def __str__(self):
        return self.title


class Award(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    award_type = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('resume:awardlist', kwargs={'rk': self.resume.pk})

    def __str__(self):
        return self.title


class School(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField()

    def get_absolute_url(self):
        return reverse('resume:schoollist', kwargs={'rk': self.resume.pk})

    def __str__(self):
        return self.name


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('resume:skilllist', kwargs={'rk': self.resume.pk})

    def __str__(self):
        return self.name
