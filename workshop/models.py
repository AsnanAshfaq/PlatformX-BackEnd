import datetime

from django.db import models
import uuid
from user.models import Organization, Student
from django.contrib.postgres.fields import ArrayField


# Create your models here.

class Workshop(models.Model):

    def get_workshop_image_path(self, filename):
        return "workshop" + "/" + str(self.id) + "/" + "poster" + "/" + str(self.topic) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Organization, related_name="workshop", on_delete=models.CASCADE)
    topic = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(blank=True)
    poster = models.ImageField(upload_to=get_workshop_image_path, default='')
    take_away = ArrayField(models.TextField(), default=list)
    event_date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(default=datetime.time, )
    end_time = models.TimeField(default=datetime.time, )
    # meeting_link = models.URLField()
    is_paid = models.BooleanField(default=False)
    charges = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class PreRequisite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    workshop = models.ForeignKey(to=Workshop, on_delete=models.CASCADE,
                                 related_name="workshop_prerequisite")
    title = models.CharField(max_length=40)
    description = models.TextField(blank=True)


class Schedule(models.Model):
    id = models.OneToOneField(to=Workshop, primary_key=True, on_delete=models.CASCADE,
                              related_name="workshop_schedule")
    time = models.TimeField(default=datetime.time)
    label = models.CharField(max_length=50)


class Participant(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="workshop_participant", default=1)
    workshop = models.ForeignKey(to=Workshop, on_delete=models.CASCADE, related_name="participant")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Speaker(models.Model):

    def get_image_path(self, filename):
        return "workshop" + "/" + str(self.id) + "/" + "speaker" + "/" + str(self.name) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    workshop = models.OneToOneField(to=Workshop, on_delete=models.CASCADE,
                                    related_name="speaker")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    image = models.ImageField(upload_to=get_image_path, default="")
    about = models.TextField()
    social_links = ArrayField(models.URLField(), default=list)


class Share(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name="workshop_share")
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="shares", null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
