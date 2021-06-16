from django.db import models
import uuid
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.core.mail import send_mail


# Create your models here.
class Hackathon(models.Model):
    # choices
    SAVED_TYPE_CHOICES = [
        ('PUBLISHED', 'PUBLISHED'),
        ('DRAFT', 'DRAFT')
    ]

    def get_thumbnail_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "thumbnail" + "/" + str(self.title) + "-" + str(filename)

    def get_background_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "background" + "/" + str(self.title) + "-" + str(filename)

    def get_logo_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "logo" + "/" + str(self.title) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.Organization', on_delete=models.CASCADE, related_name="hackathon", default=1)
    title = models.TextField(default='')
    tag_line = models.TextField(default='')
    description = models.TextField(default='')
    contact_email = models.EmailField(default='')
    theme_tags = ArrayField(models.CharField(max_length=25, blank=True), default=list)
    participant_age_required = models.IntegerField(default=1)
    is_team_required = models.BooleanField(default=False, null=False)
    rules = models.TextField(default='')
    resource = models.TextField(default='')
    submission_requirement = models.TextField(default='')
    community_chat = models.URLField(default='')
    start_of_hackathon = models.DateTimeField(default=timezone.now)
    end_of_hackathon = models.DateTimeField(default=timezone.now)
    upload_file_type = models.CharField(max_length=25, blank=False, default='')
    is_video_required = models.BooleanField(default=False)
    is_public_voting_enable = models.BooleanField(default=False)
    start_of_judging = models.DateTimeField(default=timezone.now)
    end_of_judging = models.DateTimeField(default=timezone.now)
    result_announcement_date = models.DateTimeField(default=timezone.now)
    prize_currency = models.CharField(max_length=25, default='')
    saved_type = models.CharField(max_length=10, choices=SAVED_TYPE_CHOICES, default='DRAFT')
    # IMAGES
    thumbnail_image = models.ImageField(upload_to=get_thumbnail_image_path, default='')
    logo_image = models.ImageField(upload_to=get_logo_image_path, default='')
    background_image = models.ImageField(upload_to=get_background_image_path, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Prize(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="prizes")
    title = models.CharField(max_length=25)
    value = models.IntegerField()
    no_of_winning_projects = models.IntegerField()
    description = models.TextField(default='')


class Criteria(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="criteria")
    title = models.CharField(max_length=25)
    description = models.TextField()


class Sponsor(models.Model):

    def get_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "sponsors" + "/" + str(self.name) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="sponsors")
    url = models.URLField()
    name = models.CharField(max_length=25)
    logo = models.ImageField(upload_to=get_image_path, default="", )


class Judge(models.Model):

    def get_image_path(self, filename):
        return "hackathon" + "/" + str(self.id) + "/" + "judges" + "/" + str(self.name) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE, related_name="judges")
    name = models.CharField(max_length=25)
    email = models.EmailField()
    company = models.TextField()
    photo = models.ImageField(upload_to=get_image_path, default="")
