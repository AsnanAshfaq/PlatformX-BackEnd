from django.db import models
import uuid


# Create your models here.
class Hackathon(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.User', on_delete=models.CASCADE, related_name="hackathon", default=1)
    title = models.TextField()
