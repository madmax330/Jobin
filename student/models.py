from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


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
    school = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    graduate = models.BooleanField(default=False)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    work_eligible = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)

    def get_absolute_url(self):
        if self.is_new:
            return reverse('resume:newresume')
        else:
            return reverse('student:index')

    def __str__(self):
        return self.firstname + ' ' + self.lastname
