from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from .models import Hackathon, Participant
from user.models import Student, User, Organization
from .serializer import HackathonSerializer, HackathonBriefSerializer, GetParticipantSerializer, ParticipantSerializer, \
    RegisterParticipantSerializer, GetUserHackathonsSerializer
from django.db.models import Q


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
                        hackathons_query = Hackathon.objects.exclude(id=dict(p)['hackathon']).order_by('-created_at')
                        hackathon_serializer = HackathonBriefSerializer(hackathons_query, many=True)
                        not_participated_hackathons += hackathon_serializer.data
                        return Response(data=not_participated_hackathons, status=status.HTTP_200_OK)
                    except serializers.ValidationError:
                        response['error'] = "Validation Error."
                        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            except serializers.ValidationError:
                response['error'] = "Validation Error."
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        else:
            # it means user has not applied in any hackathon
            # so simply return all of the hackathons
            try:
                # user has not applied for any hackathon
                # so return all of the hackathons
                hackathon_query = Hackathon.objects.all().order_by('-created_at')
                hackathon_serializer = HackathonBriefSerializer(hackathon_query, many=True)
                return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
            except serializers.ValidationError:
                response['error'] = "Validation Error."
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
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
        participant_serializer = RegisterParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            response['success'] = "Registration Successful"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error occurred while registering for the hackathon"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Bad request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


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
        hackathon_serializer = HackathonBriefSerializer(hackathon_query, many=True, context={"request": request})
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)

    # if request.GET['location']:
    #     location_filter_string = request.GET['q']
    #     hackathon_query = Hackathon.objects.filter(
    #         Q(title__search=hackathon_search_string) | Q(tag_line__search=location_filter_string) | Q(
    #             description__search=hackathon_search_string)).order_by(
    #         '-created_at')
    #     hackathon_serializer = HackathonBriefSerializer(hackathon_query, many=True, context={"request": request})
    #     return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)


# get hackathons of a single user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_hackathons(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        hackathon_query = Hackathon.objects.filter(user=user.id).order_by('-created_at')
        hackathon_serializer = GetUserHackathonsSerializer(hackathon_query, many=True)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error occurred while getting hackathon."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


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
