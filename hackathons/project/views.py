from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from .serializer import CreateEditProjectSerializer
from user.models import User
from hackathons.models import Project
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_project(request, id):
    response = {}
    # get student object
    user = User.objects.get(email=request.user)
    request.data['student'] = user.id
    request.data['hackathon'] = id

    request = dict(request.data)

    data = {
        **request.data
    }

    print("Data is", request)
    serializer = CreateEditProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response['success'] = "Project has been added"
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response['error'] = "Error occurred while creating project"
    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_project(request, id):
    response = {}
    # get student object
    user = User.objects.get(email=request.user)
    request.data['student'] = user.id
    request.data['hackathon'] = id
    # get project id
    query = Project.objects.get(Q(hackathon=id, student=user.id))
    serializer = ProjectSerializer(query, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response['success'] = "Project has been edited"
        response['id'] = serializer.data['id']
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response['error'] = "Error occurred while creating project"
    return Response(data=response, status=status.HTTP_200_OK)
