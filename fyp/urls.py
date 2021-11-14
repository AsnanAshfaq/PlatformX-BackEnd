from django.urls import include, path, re_path
from .views import get_all_fyps, create_fyp

urlpatterns = [
    path('fyp/create/', create_fyp),
    path('fyps/', get_all_fyps),
]
