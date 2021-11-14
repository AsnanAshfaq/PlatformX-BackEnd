from django.contrib import admin
from .models import FYP, Participant

# Register your models here.

admin.site.register([FYP, Participant])
