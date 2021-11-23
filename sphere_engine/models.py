from django.db import models
import uuid
from fyp.models import FYP
from user.models import Student
import datetime


# Create your models here.
class Test(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    fyp = models.ForeignKey(to=FYP, on_delete=models.CASCADE, related_name="test")
    name = models.TextField()
    description = models.TextField()
    event_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Submission(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    api_submission_id = models.IntegerField()
    user = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="submission")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
