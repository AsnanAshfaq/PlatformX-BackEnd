from django.contrib import admin
from .models import Workshop, Share

# Register your models here.
admin.site.register([Workshop, Share])
