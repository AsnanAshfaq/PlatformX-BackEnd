from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Hackathon, Participant
from user.models import Student, User, Organization
from .serializer import HackathonSerializer, AllHackathonSerializer, GetParticipantSerializer, ParticipantSerializer, \
    RegisterParticipantSerializer, GetUserHackathonsSerializer
from django.db.models import Q


# Create your views here.

# get all hackathons
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_hackathons(request):
    response = {}
    try:
        hackathon_query = Hackathon.objects.all()
        hackathon_serializer = AllHackathonSerializer(hackathon_query, many=True, context={"request": request})
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting hackathons."
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# get specific hackathon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_hackathon(request, id):
    hackathon_serializer = ""
    response = {}
    try:
        hackathon = Hackathon.objects.get(id=id)
        hackathon_serializer = HackathonSerializer(hackathon)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error occurred while getting hackathon."
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# searching hackathon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_hackathon(request):
    response = {}

    # fields to search -- title, tag_line, description

    if request.GET['q']:
        hackathon_search_string = request.GET['q']
        hackathon_query = Hackathon.objects.filter(
            Q(title__search=hackathon_search_string) | Q(tag_line__search=hackathon_search_string) | Q(
                description__search=hackathon_search_string)).order_by(
            '-created_at')
        hackathon_serializer = AllHackathonSerializer(hackathon_query, many=True, context={"request": request})
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)

    # if request.GET['location']:
    #     location_filter_string = request.GET['q']
    #     hackathon_query = Hackathon.objects.filter(
    #         Q(title__search=hackathon_search_string) | Q(tag_line__search=location_filter_string) | Q(
    #             description__search=hackathon_search_string)).order_by(
    #         '-created_at')
    #     hackathon_serializer = HackathonBriefSerializer(hackathon_query, many=True, context={"request": request})
    #     return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)


# get all participants of a single hackathon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_participants(request, id):
    response = {}
    try:
        participants_query = Participant.objects.filter(hackathon=id)
        participant_serializer = GetParticipantSerializer(participants_query, many=True)
        return Response(data=participant_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting participants"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# search participants of a single hackathon
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_participants(request, id):
    response = {}
    if request.GET['q']:
        participant_search_string = request.GET['q']
        # search for user's
        user_query = User.objects.filter(
            Q(first_name__search=participant_search_string) | Q(last_name__search=participant_search_string) | Q(
                username__search=participant_search_string))
        search_query = Participant.objects.filter(hackathon=id).filter(id__in=user_query)
        participant_serializer = GetParticipantSerializer(search_query, many=True)
        return Response(data=participant_serializer.data, status=status.HTTP_200_OK)

    response['error'] = "Nothing Found"
    return Response(data=response, status=status.HTTP_404_NOT_FOUND)
