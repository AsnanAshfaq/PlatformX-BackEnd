from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Hackathon
from .serializer import HackathonSerializer


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_hackathons(request):
    response = {}
    hackathon_serializer = ""
    try:
        hackathon = Hackathon.objects.all().order_by('-created_at')
        hackathon_serializer = HackathonSerializer(hackathon, many=True)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        print(hackathon_serializer)
        response['error'] = "Error occured while gettings hackathons"
        return Response(data=response, status=status.HTTP_200_OK)
