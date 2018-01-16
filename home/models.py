from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from company.models import Company


class JobinActivation(models.Model):
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=None)
    expiration = models.DateTimeField()


class JobinSchool(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobinRequestedSchool(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.name


class JobinProgram(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class JobinInvalidUser(models.Model):
    name = models.CharField(max_length=100, default='user')
    user = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


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

    def __str__(self):
        return self.extension


class JobinRequestedEmail(models.Model):
    extension = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.extension


class Notification(models.Model):
    code = models.IntegerField(default=0)
    message = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Message(models.Model):
    code = models.CharField(max_length=30)
    message = models.CharField(max_length=250)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    internal = models.BooleanField(default=True)

    def __str__(self):
        return self.message
