from django.db import models
from student.models import Student
import django.utils.timezone
from django.core.urlresolvers import reverse


class Resume(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=django.utils.timezone.now)
    file_resume = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    gpa = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    is_complete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="open")

    def get_absolute_url(self):
        if self.is_complete:
            return reverse('resume:index')
        else:
            return reverse('resume:nav', kwargs={'rk': self.pk, 'rq': 'resume_done'})

    def __str__(self):
        return self.name


class Language(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('resume:linklanguage', kwargs={'pk': self.pk, 'rk': self.rkey})

    def __str__(self):
        return self.name


class Experience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    description = models.TextField()
    company = models.CharField(max_length=100, null=True)
    experience_type = models.CharField(max_length=50)
    is_current = models.BooleanField(default=False)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('resume:linkexperience', kwargs={'pk': self.pk, 'rk': self.rkey})

    def __str__(self):
        return self.title


class Award(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    award_type = models.CharField(max_length=50)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('resume:linkaward', kwargs={'pk': self.pk, 'rk': self.rkey})

    def __str__(self):
        return self.title


class School(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='stu')
    name = models.CharField(max_length=100)
    program = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=100)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('resume:linkschool', kwargs={'pk': self.pk, 'rk': self.rkey})

    def __str__(self):
        return self.name


class Skill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('resume:linkskill', kwargs={'pk': self.pk, 'rk': self.rkey})

    def __str__(self):
        return self.name


class SchoolLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('resume:schoollist', kwargs={'rk': self.resume.pk})


class SkillLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('resume:skilllist', kwargs={'rk': self.resume.pk})


class AwardLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('resume:awardlist', kwargs={'rk': self.resume.pk})


class ExperienceLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    start = models.DateField()

    def get_absolute_url(self):
        return reverse('resume:experiencelist', kwargs={'rk': self.resume.pk})


class LanguageLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('resume:languagelist', kwargs={'rk': self.resume.pk})
