from django.contrib import admin
from .models import Hackathon, Prize, JudgingCriteria, Participant, Project

# Register your models here.

admin.site.register([Hackathon, Prize, JudgingCriteria, Participant, Project])
