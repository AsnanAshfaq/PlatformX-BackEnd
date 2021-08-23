from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import AllWorkshopSerializer
from .models import Workshop


# get all the workshops
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_workshops(request):
    response = {}
    workshop_serializer = ''
    try:
        workshop_query = Workshop.objects.all()

        workshop_serializer = AllWorkshopSerializer(workshop_query, many=True)
        return Response(data=workshop_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error while getting workshops"
        print(workshop_serializer.data)
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
