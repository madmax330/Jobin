from django.contrib import admin
from .models import JobinProgram, JobinMajor, JobinSchool, JobinTerritory, JobinBlockedEmail, JobinRequestedEmail,JobinInvalidUser

# Register your models here.
admin.site.register(JobinMajor)
admin.site.register(JobinSchool)
admin.site.register(JobinProgram)
admin.site.register(JobinTerritory)
admin.site.register(JobinBlockedEmail)
admin.site.register(JobinRequestedEmail)
admin.site.register(JobinInvalidUser)