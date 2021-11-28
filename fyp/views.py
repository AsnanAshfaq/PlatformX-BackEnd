from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Organization
from .models import Participant, FYP
from .serializer import ParticipantSerializer, CreateFYPSerializer, GetAllFYPSerializer, GetFYPSerializer, \
    GetOrganizationSerializer, CreateParticipantSerializer


# Create your views here.

# create fyp
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_fyp(request):
    response = {}
    user = User.objects.get(email=request.user)
    try:
        data = {
            **request.data,
            "user": user
        }
        serializer = CreateFYPSerializer(data=data, )
        if serializer.is_valid():
            fyp = serializer.save()
            response['success'] = "FYP has been created"
            response['id'] = fyp.id
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            print("Error is", serializer.errors)
            response["error"] = "FYP can not be created"
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        print("Error is", serializer.errors)
        response["error"] = "FYP can not be created"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_fyp(request):
    # delete the fyp
    response = {}
    try:

        user = User.objects.get_by_natural_key(username=request.user)
        if user != request.user:  # if user has not hosted the fyp
            response["error"] = "You do not have the rights to delete this FYP."
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)  # return the response with error
        fyp_query = FYP.objects.get(id=request.data['id'])
        fyp_query.delete()  # delete the fyp
        response["success"] = "FYP has been deleted"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error while deleting FYP"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get all FYP's for students
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_fyps(request):
    response = {}
    try:

        fyp_query = FYP.objects.all()
        serializer = GetAllFYPSerializer(fyp_query, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while fetching FYP's"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get a single fyp
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fyp(request, id):
    response = {}
    try:
        fyp_query = FYP.objects.get(id=id)
        serializer = GetFYPSerializer(fyp_query)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while fetching FYP"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get all fyps of organization
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_fyp(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        fyp_query = FYP.objects.filter(user=request.user.id)
        serializer = GetOrganizationSerializer(fyp_query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting FYP's"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# apply for fyp
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply(request, id):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        data = {
            "id": user.id,
            "fyp": id,
        }
        serializer = CreateParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Successfully applied for FYP"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while applying for FYP"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occurred while applying for FYP"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
