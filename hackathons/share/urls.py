from django.urls import path
from .views import create_share

urlpatterns = [
    path('create/', create_share),
]
