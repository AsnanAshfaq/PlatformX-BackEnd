import datetime

from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from user.models import Student, User
from django.core.mail import send_mail
from payment.models import Payment


# Create your models here.
class Hackathon(models.Model):

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
    theme_tags = ArrayField(models.TextField(), default=list)
    rules = ArrayField(models.TextField(), default=list)
    resource = ArrayField(models.TextField(), default=list)
    submission_requirement = models.TextField(default='')

    # media
    logo_image = models.ImageField(upload_to=get_logo_image_path, default='', blank=True)
    background_image = models.ImageField(upload_to=get_background_image_path, default='', blank=True)

    # schedule
    event_date = models.DateField(default=datetime.date.today, blank=True)

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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Evaluated(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="evaluation", default="")
    idea = models.IntegerField(default=0)
    originality = models.IntegerField(default=0)
    functionality = models.IntegerField(default=0)
    design = models.IntegerField(default=0)
    problem = models.IntegerField(default=0)
    stars = models.IntegerField(default=1)
    remarks = models.TextField(default="")


class Result(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE,
                                  related_name="result")
    first = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="first", default="")
    second = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="second", default="")
    third = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name="third", default="")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Subscription(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(
        'user.Organization', on_delete=models.CASCADE, related_name="subscription", default=1)
    plan = models.TextField()
    payment_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
