from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Organization
from .models import Test, Submission
from fyp.models import FYP, Participant
from .serializer import CreateEditTestSerializer, GetTestSerializer
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test(request, id):
    response = {}
    try:
        test_query = Test.objects.get(fyp=id)
        if test_query.exists():
            serializer = GetTestSerializer(test_query)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    except Test.DoesNotExist as e:
        response['error'] = 'Error while getting Test'
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
