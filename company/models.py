from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100)
    points = models.IntegerField()
    logo = models.FileField(null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)
    is_new = models.BooleanField(default=True)
    is_startup = models.BooleanField(default=False)
    industry = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Suggestion(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    topic = models.CharField(max_length=100)
    suggestion = models.TextField()
    importance = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    priority = models.IntegerField(null=True, blank=True)
    resolved = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    open = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic
