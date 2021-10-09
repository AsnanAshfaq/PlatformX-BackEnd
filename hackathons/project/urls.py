from django.urls import path, include
from .views import create_project, edit_project

urlpatterns = [
    path('create/', create_project),
    path('edit/', edit_project)
]
