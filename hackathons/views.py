from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Hackathon
from user.models import Student, User
from .serializer import HackathonSerializer, HackathonBriefSerializer, ParticipantSerializer


# Create your views here.

# get all hackathons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_hackathons(request):
    response = {}
    hackathon_serializer = ""
    try:
        hackathon = Hackathon.objects.all().order_by('-created_at')
        hackathon_serializer = HackathonBriefSerializer(hackathon, many=True)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occured while getting hackathons."
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# get specific hackathon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hackathon(request, id):
    print("id is", id)
    hackathon_serializer = ""
    response = {}
    try:
        hackathon = Hackathon.objects.get(id=id)
        hackathon_serializer = HackathonSerializer(hackathon)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error occured while getting hackathon."
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# register hackathon
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request, id):
    try:
        student = Student.objects.get(uuid=request.user)
        data = {
            "id": student.uuid,
            "hackathon": id
        }
        response = {}
        participant_serializer = ParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            print("Serializer is valid")
            participant_serializer.save()
            response['success'] = "Registration Successful"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            print("Serializer is not valid")
            print(participant_serializer.errors)
            response['error'] = "Error while registring for the hackathon"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Bad request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
