from django.contrib import admin
from .models import JobinProgram, JobinMajor, JobinSchool, JobinTerritory

# Register your models here.
admin.site.register(JobinMajor)
admin.site.register(JobinSchool)
admin.site.register(JobinProgram)
admin.site.register(JobinTerritory)