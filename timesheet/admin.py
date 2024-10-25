from django.contrib import admin
from .models import Project, Timesheet, Profile

admin.site.register(Project)
admin.site.register(Timesheet)
admin.site.register(Profile)
