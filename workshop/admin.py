from django.contrib import admin
from .models import Workshop, Share, Participant, Schedule, Speaker

# Register your models here.
admin.site.register([Workshop, Share, Participant, Schedule, Speaker])
