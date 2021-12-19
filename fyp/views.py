from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Organization
from .models import Participant, FYP
from .serializer import ParticipantSerializer, CreateFYPSerializer, GetAllFYPSerializer, GetFYPSerializer, \
    GetOrganizationSerializer, CreateEditParticipantSerializer
from .zoom import ZoomAPI
from .mail import Mail
from django.db.models import Q


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
        serializer = GetFYPSerializer(fyp_query, context={"request": request})
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
        fyp_query = FYP.objects.filter(user=user.id)
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

        participant_query = Participant.objects.filter(user=user.id, fyp=id)
        if participant_query.exists():
            response['error'] = "Error occurred while register for workshop"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "user": user.id,
            "fyp": id,
        }
        serializer = CreateEditParticipantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Successfully applied for FYP"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while applying for FYP"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occurred while applying for FYP"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# schedule meeting
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def schedule_meeting(request, id, stdid):
    response = {}
    try:

        schedule_time = request.data['date']
        zoom = ZoomAPI(fyp=id, std_id=stdid, time=schedule_time)
        participant_query = Participant.objects.get(fyp=id, user=stdid)

        if zoom.create_meeting() == 1:
            zoom_response = zoom.get_response()

            mail = Mail(data=zoom.get_response, applicant_id=stdid, fyp=id)
            mail.send_mail_to_applicant(join_url=zoom_response['join_url'], join_time=zoom_response['start_time'])
            mail.send_mail_to_organization(start_url=zoom_response['start_url'], join_time=zoom_response['start_time'])

            participant_query.is_meeting_scheduled = True
            participant_query.meeting_schedule = schedule_time
            participant_query.join_url = zoom_response['join_url']
            participant_query.save()
            response['success'] = "Interview has been scheduled."
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while scheduling interview"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occurred while scheduling interview"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_fyp(request):
    response = []
    try:

        user_query = dict(request.GET)
        if "q" in user_query.keys():
            fyp_search_string = request.GET['q']
            searching_query = FYP.objects.filter(
                Q(name__icontains=fyp_search_string) | Q(description__icontains=fyp_search_string)).order_by(
                '-created_at')
            fyp_serializer = GetAllFYPSerializer(searching_query, many=True, context={"request": request})
            # response.append(fyp_serializer.data)
            response += fyp_serializer.data

        if "categories" in user_query.keys():
            print("Filtering for categories")
            fyp_query = FYP.objects.filter(category__contains=user_query['categories']).order_by(
                '-created_at')
            if fyp_query.exists():
                fyp_serializer = GetAllFYPSerializer(fyp_query, many=True, context={"request": request})
                # response.append(fyp_serializer.data)
                response += fyp_serializer.data

        if "technologies" in user_query.keys():
            fyp_query = FYP.objects.filter(technologies__contains=user_query['technologies']).order_by(
                '-created_at')

            if fyp_query.exists():
                print("Tech filter exists", fyp_query)
                fyp_serializer = GetAllFYPSerializer(fyp_query, many=True, context={"request": request})
                # response.append(fyp_serializer.data)
                response += fyp_serializer.data

        if len(response) > 0:  # because we have one empty element
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {'error': "No fyp found."}
            return Response(data=response, status=status.HTTP_200_OK)
    except:
        response = {'error': "Error occurred while searching fyps."}
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
