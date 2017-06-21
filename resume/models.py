from django.db import models
from student.models import Student


class Resume(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_updated = models.DateTimeField()
    file_resume = models.FileField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    gpa = models.FloatField(default=0, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="open")

    def __str__(self):
        return self.name


class Language(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

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

    def __str__(self):
        return self.name


class Skill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    rkey = models.CharField(max_length=20)
    rname = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reference(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    affiliation = models.CharField(max_length=200)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SchoolLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'school')


class SkillLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'skill')


class AwardLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'award')


class ExperienceLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    start = models.DateField()

    class Meta:
        unique_together = ('resume', 'experience')


class LanguageLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'language')


class ReferenceLink(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resume', 'reference')
