from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
import uuid


# custom model manager

class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        user.password = make_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser = True")

        return self._create_user(username, email, password, **extra_fields)


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, unique=True, editable=False)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    email = models.EmailField(_('email address'), blank=False, unique=True, )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # custom manager
    objects = CustomUserManager()


class Student(models.Model):
    uuid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    education = models.CharField(max_length=80)
    bio = models.CharField(max_length=80)
    lives_in = models.CharField(max_length=80)
    skills = ArrayField(models.CharField(max_length=20, blank=True))
    interests = ArrayField(models.CharField(max_length=20, blank=True))

    def save(self, *args, **kwargs):
        if hasattr(self.uuid, 'organization'):
            return
        super().save(*args, **kwargs)


class Organization(models.Model):
    uuid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="organization")
    reg_no = models.IntegerField()
    location = models.CharField(max_length=80)

    def save(self, *args, **kwargs):
        if hasattr(self.uuid, 'student'):
            return
        super().save(*args, **kwargs)


class Follower(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4, unique=True, editable=False)
    follower_id = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
    followed_id = models.ForeignKey(User, related_name='followed_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ProfileImage(models.Model):
    def get_image_path_and_filename(self, filename):
        return "user_images" + "/profile_images/" + str(self.id) + "/" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile_image", null=False)
    metadata = models.CharField(max_length=30, default="", null=True, blank=True)
    path = models.ImageField(upload_to=get_image_path_and_filename, default="", )

    def __str__(self):
        return str(self.metadata)


class BackgroundImage(models.Model):
    def get_image_path_and_filename(self, filename):
        return "user_images" + "/background_images/" + str(self.id) + "/" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_background_image", null=False)
    metadata = models.CharField(max_length=30, default="", null=True, blank=True)
    path = models.ImageField(upload_to=get_image_path_and_filename, default="", )

    def __str__(self):
        return str(self.metadata)
