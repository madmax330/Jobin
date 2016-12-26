from django.db import models
from company.models import Company
from student.models import Student
from django.core.urlresolvers import reverse


class Event(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    active = models.BooleanField(default=True)
    schools = models.CharField(max_length=200, null=True, default='ALL')
    programs = models.CharField(max_length=200, null=True, default='ALL')
    website = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)

    def get_absolute_url(self):
        return reverse('event:companyevent', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class EventInterest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date = models.DateField()
    event_name = models.CharField(max_length=100, null=True)






