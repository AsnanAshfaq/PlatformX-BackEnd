from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Hackathon, Participant
from user.models import Student, User
from .serializer import HackathonSerializer, HackathonBriefSerializer, ParticipantSerializer


# i want to get all the hackathons where student.uuid is not a participant of
# Create your views here.

# get all hackathons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_hackathons(request):
    response = {}
    hackathon_serializer = ""
    try:
        # get all the hackathons in which student has not yet applied
        # first get user id
        user = User.objects.get(email=request.user)
        # get list of hackathons where user is part of
        is_participant = Participant.objects.filter(id=user.id)
        if len(list(is_participant)) > 0:  # if we got the list of hackathons where student has applied
            try:
                # it means user has applied in some of the hackathons
                participant_serializer = ParticipantSerializer(is_participant, many=True)
                not_participated_hackathons = []  # initialize array
                for p in list(participant_serializer.data):  # loop through the list of data in participant
                    try:
                        # now get hackathons where user has not applied
                        hackathons = Hackathon.objects.exclude(id=dict(p)['hackathon']).order_by('-created_at')
                        hackathon_serializer = HackathonBriefSerializer(hackathons, many=True)
                        not_participated_hackathons += hackathon_serializer.data
                        return Response(data=not_participated_hackathons, status=status.HTTP_200_OK)
                    except(serializers.ValidationError):
                        response['error'] = "Validation Error."
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            except(serializers.ValidationError):
                response['error'] = "Validation Error."
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            # it means user has not applied in any hackathon
            # so simply return all of the hackathons
            try:
                # user has not applied for any hackathon
                # so return all of the hackathons
                hackathon = Hackathon.objects.all().order_by('-created_at')
                hackathon_serializer = HackathonBriefSerializer(hackathon, many=True)
                return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
            except(serializers.ValidationError):
                response['error'] = "Validation Error."
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
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
        student = User.objects.get(email=request.user)
        data = {
            "id": student.id,
            "hackathon": id
        }
        response = {}
        participant_serializer = ParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            response['success'] = "Registration Successful"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error while registering for the hackathon"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Bad request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
