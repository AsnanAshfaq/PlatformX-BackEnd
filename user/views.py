from django.shortcuts import render
from rest_framework import (viewsets, permissions, generics, status)
from .models import User, Student
from .serializer import UserSerializer, StudentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StudentViewSet(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user(request):
    try:
        print("trying to get")
        user = User.objects.all()
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        print("excepting")
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    try:
        print("trying to get")
        user = User.objects.get(id="8d86d889-ae08-4d4d-bb6b-e39af80c5590")
        serializer = UserSerializer(data=user)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        print("excepting")
        return Response(status=status.HTTP_404_NOT_FOUND)
