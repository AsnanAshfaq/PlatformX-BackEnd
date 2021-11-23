from django.contrib import admin
from .models import Test, Submission

# Register your models here.

admin.site.register([Test, Submission])
