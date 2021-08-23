from django.db import models
import uuid
from user.models import Organization, Student


# Create your models here.

class Workshop(models.Model):

    def get_workshop_image_path(self, filename):
        return "workshop" + "/" + str(self.id) + "/" + "poster" + "/" + str(self.title) + "-" + str(filename)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(Organization, related_name="workshop", on_delete=models.CASCADE)
    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.TextField(max_length=255, blank=True, )
    poster = models.ImageField(upload_to=get_workshop_image_path, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Participant(models.Model):
    id = models.OneToOneField(to=Student, primary_key=True, on_delete=models.CASCADE,
                              related_name="workshop_participant")
    workshop = models.ForeignKey(to=Workshop, on_delete=models.CASCADE,
                                 related_name="participant")
    join_date = models.DateTimeField(auto_now_add=True)
