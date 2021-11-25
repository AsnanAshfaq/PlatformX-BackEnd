from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from user.models import User, Organization
from .models import Internship, Participant
from fyp.models import FYP, Participant
from .serializer import GetAllInternshipSerializer
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_internships(request):
    response = {}
    try:
        query = Internship.objects.all()
        serializer = GetAllInternshipSerializer(query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting internship"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_internship(request):
    response = {}
    try:
        query = Internship.objects.all()
        serializer = GetAllInternshipSerializer(query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting internship"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
