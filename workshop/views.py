from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import AllWorkshopSerializer, GetWorkshopSerializer
from .models import Workshop
from django.db.models import Q


# get all the workshops
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshops(request):
    response = {}
    workshop_serializer = ''
    try:
        workshop_query = Workshop.objects.all()
        workshop_serializer = AllWorkshopSerializer(workshop_query, many=True)
        return Response(data=workshop_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting workshops"
        print(workshop_serializer.data)
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
