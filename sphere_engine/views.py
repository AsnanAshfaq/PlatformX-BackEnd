from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Organization
from .models import Test, Submission
from fyp.models import FYP, Participant
from .serializer import CreateEditTestSerializer, GetTestSerializer, GetAllSubmissionSerializer, \
    GetSubmissionSerializer, CreateSubmissionSerializer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_test(request):
    response = {}

    try:
        # get fyp id
        fyp_query = FYP.objects.get(id=request.data['fyp_id'])
        data = {
            **request.data,
            "fyp": fyp_query.id
        }
        serializer = CreateEditTestSerializer(data=data)
        if serializer.is_valid():
            # save test
            serializer.save()
            response['success'] = "Test has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while creating test"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occurred while creating test"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_submission(request):
    response = {}
    submission_id = request.data['submission_id']
    fyp_id = request.data['fyp_id']
    try:
        user = User.objects.get(email=request.user)
        fyp = FYP.objects.get(id=fyp_id)
        data = {
            "fyp": fyp.id,
            "user": user,
            "api_submission_id": submission_id
        }
        serializer = CreateSubmissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Your code has been submitted"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while submitting code"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Error occured while submitting code"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test(request, id):
    response = {}
    try:
        test_query = Test.objects.get(fyp=id)
        if test_query:
            serializer = GetTestSerializer(test_query)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    except Test.DoesNotExist as e:
        response['error'] = 'Error while getting Test'
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_submission(request, id):
    response = {}
    try:

        submission_query = Submission.objects.filter(fyp=id)
        if submission_query.exists():
            serializer = GetAllSubmissionSerializer(submission_query, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        response['error'] = "Error while getting Submissions"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error while getting Submissions"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get single submission of a fyp
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_submission(request, fypID, submissionID):
    response = {}
    try:

        submission_query = Submission.objects.get(fyp=fypID, id=submissionID)
        if submission_query:
            serializer = GetSubmissionSerializer(submission_query)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        response['error'] = "Error while getting Submissions"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error while getting Submissions"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
