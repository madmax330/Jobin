from django.db import models
from student.models import Student
from company.models import Company


class JobinSchool(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class JobinProgram(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobinMajor(models.Model):
    program = models.ForeignKey(JobinProgram, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notification(models.Model):
    priority = models.CharField(max_length=50)
    message = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return self.date
