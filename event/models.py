from django.db import models
from company.models import Company
from student.models import Student
from django.core.urlresolvers import reverse


class Event(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    active = models.BooleanField(default=True)
    schools = models.CharField(max_length=200, default='ALL')
    programs = models.CharField(max_length=200, default='ALL')
    website = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    description = models.TextField()
    times_saved = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('event:companyevent', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class SavedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    date = models.DateField()
    event_name = models.CharField(max_length=100)






