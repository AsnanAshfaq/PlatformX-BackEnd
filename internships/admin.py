from django.contrib import admin
from .models import Internship, Participant

# Register your models here.

admin.site.register([Internship, Participant])
