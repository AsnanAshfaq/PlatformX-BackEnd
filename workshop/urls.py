from django.urls import include, path
from rest_framework import routers
from .views import get_workshops
from rest_framework.authtoken import views

urlpatterns = [
    # path('workshop/', get_user_workshops),
    path('workshops/', get_workshops),
]
