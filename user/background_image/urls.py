from django.urls import path
from .views import create_background_image, edit_background_image, delete_background_image

urlpatterns = [
    path('create/', create_background_image),
    path('edit/', edit_background_image),
    path('delete/', delete_background_image),
]
