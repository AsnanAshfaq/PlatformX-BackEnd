from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .serializer import AllWorkshopSerializer, GetWorkshopSerializer, CreateEditWorkshopSerializer, \
    GetWorkshopParticipantSerializer, CreateParticipantSerializer
from .models import Workshop, Participant
from django.db.models import Q
from user.models import User, Organization
from .zoom import ZoomAPI
from .mail import Mail
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


# create workshop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_workshop(request):
    response = {}
    try:
        # create workshop
        user = User.objects.get(email=request.user)

        data = {
            **request.data,
            "user": user
        }
        serializer = CreateEditWorkshopSerializer(data=data)
        if serializer.is_valid():
            workshop = serializer.save()
            response['id'] = workshop.id
            response['success'] = "Workshop has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        response['error'] = "Error while creating workshop"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        print(serializer.errors)
        response['error'] = "Error while creating workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# update a workshop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_workshop(request):
    response = {}

    try:
        # find worshop
        workshop_query = Workshop.objects.get(id=request.data['id'])
        data = {
            **request.data,
        }

        serializer = CreateEditWorkshopSerializer(workshop_query, data=data)
        if serializer.is_valid():
            # send mail to all the participants that the workshop has been edited
            workshop = serializer.save()
            response['id'] = workshop.id
            response['success'] = "Workshop has been edited"
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer, status=status.HTTP_201_CREATED)
    except:
        response['error'] = "Error while updating workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# start the workshop
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_workshop(request):
    response = {}
    # check if the user making the request is organization or not
    user_id = User.objects.get(email=request.user)
    organization_query = Organization.objects.filter(uuid=user_id)
    if organization_query:
        zoom = ZoomAPI(workshop=request.data['id'])
        if zoom.create_meeting() == 1:
            zoom_response = zoom.get_response()
            mail = Mail(workshop=request.data['id'], data=zoom_response)
            # send mail to all the participants
            mail.send_mail_to_attendees()
            response['success'] = "Meeting created successfully"
            return Response(data=zoom_response(), status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while creating meeting"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    # user is not valid
    response['error'] = "Invalid User"
    return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


# get all the workshops
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshops(request):
    response = {}
    try:
        workshop_query = Workshop.objects.all()
        workshop_serializer = AllWorkshopSerializer(workshop_query, many=True, context={"request": request})
        return Response(data=workshop_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting workshops"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get a single workshop
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshop(request, id):
    response = {}
    try:
        workshop_query = Workshop.objects.get(id=id)
        serializer = GetWorkshopSerializer(workshop_query, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        print(serializer)
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


# get participants of the workshop
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_participants(request, id):
    response = {}
    user = User.objects.get_by_natural_key(username=request.user)
    if user != request.user:  # if user has not hosted the fyp
        response["error"] = "Invalid User Type."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)  # return the response with error
    try:

        participant_query = Participant.objects.filter(workshop=id)
        serializer = GetWorkshopParticipantSerializer(participant_query, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting workshop participants"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_paid_workshop(request, id):
    response = {}

    try:
        user = User.objects.get(email=request.user)
        participant_query = Participant.objects.filter(id=user.id, workshop=id)

        # check if user has not participated in the workshop
        if participant_query.exists():
            response['error'] = "Error occurred while register for workshop"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            # make stripe payment
            amount = request.data['charges'] * 100 * 0.43
            # 100 is for cents and 0.43 is for conversion from indian rupees to pakistan
            description = request.data['description']

            stripe_response = stripe.Charge.create(
                amount=int(amount),
                currency="inr",
                source="tok_visa",
                description=description,
                receipt_email=user.email
            )

            # add user as participant to workshop
            serializer_data = {
                "id": user.id,
                "workshop": id
            }

            serializer = CreateParticipantSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                response['success'] = "Registration successful"
                return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "Error occurred while register for workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

    except:
        response['error'] = "Error occurred while register for workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_workshop(request, id):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        participant_query = Participant.objects.filter(id=user.id, workshop=id)

        # check if user has not participated in the workshop
        if participant_query.exists():
            response['error'] = "Error occurred while register for workshop"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            # add user as participant to workshop
            serializer_data = {
                "id": user.id,
                "workshop": id
            }
            serializer = CreateParticipantSerializer(data=serializer_data)
            if serializer.is_valid():
                serializer.save()
                response['success'] = "Registration successful"
                return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "Error occurred while register for workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

    except:
        response['error'] = "Error occurred while register for workshop"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
