import datetime

from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from user.models import Student, User
from django.core.mail import send_mail


# Create your models here.
class Hackathon(models.Model):
    # choices
    SAVED_TYPE_CHOICES = [
        ('PUBLISHED', 'PUBLISHED'),
        ('DRAFT', 'DRAFT')
    ]
    STATUS = [
        ('Upcoming', 'Upcoming'),
        ('Open', 'Open'),
        ('Ended', 'Ended')
    ]

    def get_background_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "background" + "/" + str(self.title) + "-" + str(filename)

    def get_logo_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "logo" + "/" + str(self.title) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.Organization', on_delete=models.CASCADE, related_name="hackathon", default=1)

    # general
    title = models.TextField(default='')
    tag_line = models.TextField(default='')
    description = models.TextField(default='')
    theme_tags = ArrayField(models.CharField(max_length=25, blank=True), default=list)
    rules = ArrayField(models.TextField(), default=list)
    resource = ArrayField(models.TextField(), default=list)
    submission_requirement = ArrayField(models.TextField(), default=list)

    # media
    logo_image = models.ImageField(upload_to=get_logo_image_path, default='', blank=True)
    background_image = models.ImageField(upload_to=get_background_image_path, default='', blank=True)
    is_video_required = models.BooleanField(default=False, blank=True)

    # schedule
    start_date_of_hackathon = models.DateField(default=datetime.date.today, blank=True)
    start_time_of_hackathon = models.TimeField(default=datetime.time, blank=True)
    end_date_of_hackathon = models.DateField(default=datetime.date.today, blank=True)
    end_time_of_hackathon = models.TimeField(default=datetime.time, blank=True)

    saved_type = models.CharField(max_length=10, choices=SAVED_TYPE_CHOICES, default='DRAFT', blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='Upcoming', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Prize(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="prizes")
    title = models.CharField(max_length=25)  # first, second, third
    value = models.IntegerField()  # prize money


class JudgingCriteria(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="hackathon_judging_criteria")
    title = models.TextField()
    description = models.TextField()


class Participant(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="hackathon_participant", default=1)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE,
                                  related_name="participant")
    join_date = models.DateTimeField(auto_now_add=True)




class Project(models.Model):
    def get_logo_image_path(self, filename):
        return "hackathon" + "/" + "project" + "/" + str(self.id) + "/" + "logo" + "/" + str(self.title) + "-" + str(
            filename)

    def get_file_path(self, filename):
        return "hackathon" + "/" + "project" + "/" + str(self.id) + "/" + "file" + "/" + str(self.title) + "-" + str(
            filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name="project", default="")
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE,
                                  related_name="project")
    title = models.TextField(default='')
    description = models.TextField(default='')
    tag_line = models.TextField(default='')
    about = models.TextField(default='')
    built_with = ArrayField(models.TextField(max_length=25, default=""), blank=True, default=list)
    links = models.URLField()
    video_link = models.URLField(default="", blank=True)
    logo = models.ImageField(upload_to=get_logo_image_path, default='', blank=True)
    file = models.FileField(default="", upload_to=get_file_path)
