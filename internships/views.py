from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from user.models import User, Organization
from .models import Internship, Participant
from .serializer import GetAllInternshipSerializer, GetInternshipSerializer, CreateEditParticipantSerializer, \
    GetInternshipParticipantsSerializer, GetOrganizationSerializer, CreateEditInternshipSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from .zoom import ZoomAPI
from .mail import Mail
from django.core.mail import BadHeaderError
from smtplib import SMTPException
from datetime import datetime
from django.db.models import Q


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_internship(request):
    response = {}
    try:

        user = User.objects.get(email=request.user)

        data = {
            "user": user.id,
            **request.data
        }

        serializer = CreateEditInternshipSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Internship has been created Successfully"
            return Response(data=response, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        response['error'] = "Error occurred while creating Internship"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        print(serializer.errors)
        response['error'] = "Error occurred while creating Internship"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# get all internships for students
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_internships(request):
    response = {}
    try:
        query = Internship.objects.all()
        serializer = GetAllInternshipSerializer(query, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting internship"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get single internship

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_internship(request, id):
    response = {}
    try:
        query = Internship.objects.get(id=id)
        serializer = GetInternshipSerializer(query, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting internship"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get organization internships
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_internship(request):
    response = {}
    try:
        query = Internship.objects.all()
        serializer = GetOrganizationSerializer(query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting internship"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# apply for the internship
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def apply(request, id):
    response = {}

    try:
        # get internship and user id
        internship_query = Internship.objects.get(id=id)
        user = User.objects.get(email=request.user)
        request = dict(request.data)
        data = {
            "id": user,
            "internship": internship_query.id,
            "github": request['github'][0],
            "linked_in": request['linked_in'][0],
            "cv": request['cv'][0],
        }
        serializer = CreateEditParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Successfully applied for the internship"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while applying for internship"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occurred while applying for internship"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_internship_applicants(request, id):
    response = {}
    try:
        participant_query = Participant.objects.filter(internship=id)
        serializer = GetInternshipParticipantsSerializer(participant_query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while getting applicants"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_internship_applicant(request, id, stdid):
    response = {}
    try:
        participant_query = Participant.objects.get(internship=id, id=stdid)
        serializer = GetInternshipParticipantsSerializer(participant_query)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while getting applicants"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_meeting(request, id, stdid):
    response = {}
    try:

        schedule_time = request.data['time']
        zoom = ZoomAPI(internship=id, std_id=stdid, time=schedule_time)
        if zoom.create_meeting() == 1:
            zoom_response = zoom.get_response()
            mail = Mail(data=zoom.get_response, applicant_id=stdid, internship_id=id)
            # send mail to applicant
            join_time = schedule_time
            mail.send_mail_to_applicant(join_url=zoom_response['join_url'], join_time=join_time)
            mail.send_mail_to_organization(start_url=zoom_response['start_url'], join_time=join_time)

            # adding meeting details to participant model
            # participant_query = Participant.objects.get(internship=id, id=stdid)
            data = {
                "meeting_id": zoom_response['uuid'],
                "is_meeting_scheduled": True,
                "meeting_schedule": schedule_time
            }
            # serializer = CreateEditParticipantSerializer(participant_query,data=data)
            # if serializer.is_valid():
            response['success'] = "Interview has been scheduled."
            return Response(data=response, status=status.HTTP_201_CREATED)

    except BadHeaderError:
        response['error'] = "Invalid mail format"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except SMTPException as e:
        response['error'] = "Error occurred while scheduling interview"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occurred while scheduling interview"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_internship(request):
    response = []

    try:
        user_query = dict(request.GET)
        print("Query is", user_query)
        if "q" in user_query.keys():
            internship_search_string = request.GET['q']
            searching_query = Internship.objects.filter(
                Q(name__icontains=internship_search_string)).order_by(
                '-created_at')
            internship_serializer = GetAllInternshipSerializer(searching_query, many=True, context={"request": request})
            response += internship_serializer.data

        if "duration" in user_query.keys():
            internship_search_string = request.GET['duration']
            searching_query = Internship.objects.filter(
                Q(duration__icontains=internship_search_string)).order_by(
                '-created_at')
            internship_serializer = GetAllInternshipSerializer(searching_query, many=True, context={"request": request})
            response += internship_serializer.data

        if len(response) > 0:
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {'error': "No internship found."}
            return Response(data=response, status=status.HTTP_200_OK)

    except:
        response = {'error': "Error occurred while searching fyps."}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
