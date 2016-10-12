from django.db import models
from student.models import Student
from company.models import Company


class JobinSchool(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

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


class JobinTerritory(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class JobinBlockedEmail(models.Model):
    extension = models.CharField(max_length=50)


class JobinRequestedEmail(models.Model):
    extension = models.CharField(max_length=50)


class Notification(models.Model):
    code = models.IntegerField(default=0)
    message = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True, auto_now_add=True)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Message(models.Model):
    code = models.CharField(max_length=30)
    message = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    internal = models.BooleanField(default=True)

    def __str__(self):
        return self.message
