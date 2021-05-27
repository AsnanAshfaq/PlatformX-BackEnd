from django.shortcuts import render
from rest_framework import (viewsets, permissions, generics, status)
from .models import User, Student
from .serializer import UserSerializer, StudentSerializer


# Create your views here.

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentViewSet(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
