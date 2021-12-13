from django.db import models
import uuid
from user.models import Organization, Student, User
from django.contrib.postgres.fields import ArrayField
from datetime import date


# Create your models here.
class FYP(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('user.Organization', related_name="fyp", on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = ArrayField(models.TextField(), default=list)
    technologies = ArrayField(models.TextField(), default=list)
    outcomes = models.TextField()
    team_members = models.IntegerField(default=1)
    end_date = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Participant(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="fyp_participant", default=1)
    fyp = models.ForeignKey(to=FYP, on_delete=models.CASCADE, related_name="participant")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_meeting_scheduled = models.BooleanField(default=False)
    meeting_schedule = models.DateTimeField(default=date.today)
    meeting_id = models.IntegerField(default=0)
    join_url = models.TextField(default="")
