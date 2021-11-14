from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User
from .models import Participant, FYP
from .serializer import ParticipantSerializer, CreateFYPSerializer, GetAllFYPSerializer


# Create your views here.

# create fyp
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_fyp(request):
    response = {}
    try:

        return Response(data=response, status=status.HTTP_201_CREATED)
    except:
        response["error"] = "FYP can not be created"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# get all fyps
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_fyps(request):
    response = {}
    try:

        fyp_query = FYP.objects.all()
        serializer = GetAllFYPSerializer(fyp_query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while fetching FYP's"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
