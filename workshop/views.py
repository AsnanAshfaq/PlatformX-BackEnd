from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import AllWorkshopSerializer, GetWorkshopSerializer
from .models import Workshop
from django.db.models import Q
from user.models import User, Organization
import requests

from .zoom import Zoom


# create workshop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_workshop(request):
    response = {}
    try:
        return Response(data=response, status=status.HTTP_201_CREATED)
    except:
        response['error'] = "Error while getting workshops"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# start the workshop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_workshop(request):
    response = {}
    # check if the user making the request is organization or not
    user_id = User.objects.get(email=request.user)
    organization_query = Organization.objects.filter(uuid=user_id)
    if organization_query:
        zoom = Zoom(workshop=request.data['id'])
        value = zoom.create_meeting()
        if value == 1:
            response['success'] = "Meeting created successfully"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while creating meeting"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    # user is not valid
    response['error'] = "Invalid User"
    return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# get all the workshops
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshops(request):
    response = {}
    try:
        workshop_query = Workshop.objects.all()
        workshop_serializer = AllWorkshopSerializer(workshop_query, many=True)
        return Response(data=workshop_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting workshops"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get a single workshop
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshop(request, id):
    response = {}
    try:
        fyp_query = Workshop.objects.get(id=id)
        serializer = GetWorkshopSerializer(fyp_query)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while fetching workshop"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# searching post
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_workshop(request):
    response = {}

    if request.GET['q']:
        workshop_search_string = request.GET['q']
        workshop_query = Workshop.objects.filter(
            Q(title__search=workshop_search_string) | Q(description__search=workshop_search_string)).order_by(
            '-created_at')
        workshop_serializer = AllWorkshopSerializer(workshop_query, many=True, context={"request": request})
        return Response(data=workshop_serializer.data, status=status.HTTP_200_OK)
