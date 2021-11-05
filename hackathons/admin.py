from django.contrib import admin
from .models import Hackathon, Judge, Prize, JudgingCriteria, Participant, Share, Project, Team, ProjectMedia

# Register your models here.

admin.site.register([Hackathon, Judge, Prize, JudgingCriteria, Participant, Share, Project, ProjectMedia, Team])
