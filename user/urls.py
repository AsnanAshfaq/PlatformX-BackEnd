from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, StudentViewSet, get_user, list_user
from rest_framework.authtoken import views

urlpatterns = [
    path('all/', UserViewSet.as_view()),
    path('student/', StudentViewSet.as_view()),
    path('<uuid:id>/', get_user),
    path('all/', list_user)
]
