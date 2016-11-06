from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=256, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=25, null=True)
    zipcode = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    points = models.IntegerField(null=True)
    logo = models.FileField(null=True, blank=True)
    website = models.CharField(max_length=256, null=True)
    is_new = models.BooleanField(default=True)
    is_startup = models.BooleanField(default=False)

    def get_absolute_url(self):
        if self.is_new:
            return reverse('company:details', kwargs={'pk': self.pk})
        else:
            return reverse('company:index')

    def __str__(self):
        return self.name
