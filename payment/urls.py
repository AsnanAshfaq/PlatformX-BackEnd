from django.urls import path, include
from .views import create_payment, get_student_payments

urlpatterns = [
    path('create/', create_payment),
    path('all/', get_student_payments),
]
