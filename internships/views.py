from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from user.models import User, Organization
from .models import Internship, Participant
from .serializer import GetAllInternshipSerializer, GetInternshipSerializer, CreateParticipantSerializer, \
    GetInternshipParticipantsSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser
from .zoom import ZoomAPI


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_internship(request):
    pass


# get all internships for students
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_internships(request):
    response = {}
    try:
        query = Internship.objects.all()
        serializer = GetAllInternshipSerializer(query, many=True)
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
        serializer = GetInternshipSerializer(query)
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
        serializer = GetAllInternshipSerializer(query, many=True)
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
        serializer = CreateParticipantSerializer(data=data)
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
        zoom = ZoomAPI(internship=id, std_id=stdid, time=request.data['time'])
        print(zoom.create_meeting())
        if zoom.create_meeting() == 1:
            zoom_response = zoom.get_response()
            return Response(data=zoom_response, status=status.HTTP_201_CREATED)
        return Response(data=response, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while scheduling interview"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
