from django.db import models
import uuid
from user.models import Organization, Student, User
from django.contrib.postgres.fields import ArrayField
from datetime import date


# Create your models here.

class Internship(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('user.Organization', related_name="internship", on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    skills = ArrayField(models.TextField(), default=list)
    responsibilities = ArrayField(models.TextField(), default=list)
    duration = models.IntegerField()
    working_hour = models.IntegerField()
    is_certificate = models.BooleanField()
    end_date = models.DateField(default=date.today)
    stipend = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Participant(models.Model):
    id = models.OneToOneField(to=Student, primary_key=True, on_delete=models.CASCADE,
                              related_name="internship_participant")
    internship = models.ForeignKey(to=Internship, on_delete=models.CASCADE, related_name="participant")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
