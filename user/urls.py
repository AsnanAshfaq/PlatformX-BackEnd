from django.urls import include, path
from rest_framework import routers
from .views import get_user, get_all_users
from rest_framework.authtoken import views

urlpatterns = [
    path('', get_user),
    path('all/', get_all_users),
]
