from django.db import models
import uuid


# Create your models here.
class Payment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        'user.Organization', on_delete=models.CASCADE, related_name="payment", default=1)


