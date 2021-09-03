from django.urls import path
from .views import create_profile_image

urlpatterns = [
    path('create/', create_profile_image),
]
