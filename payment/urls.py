from django.urls import path, include
from .views import create_payment

urlpatterns = [
    path('create/', create_payment),
]
