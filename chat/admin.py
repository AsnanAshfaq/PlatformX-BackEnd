from django.contrib import admin
from .models import Chat, Message, ChannelModel

# Register your models here.
admin.site.register([Message, Chat, ChannelModel])
