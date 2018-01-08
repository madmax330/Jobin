from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True)
    name = models.CharField(max_length=200)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    school = models.CharField(max_length=100, null=True, blank=True)
    program = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    graduate = models.BooleanField(default=False)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    work_eligible = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    transcripts = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname
