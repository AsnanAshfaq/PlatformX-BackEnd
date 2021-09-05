from django.urls import path
from .views import create_profile_image, edit_profile_image, delete_profile_image

urlpatterns = [
    path('create/', create_profile_image),
    path('edit/', edit_profile_image),
    path('delete/', delete_profile_image),
]
