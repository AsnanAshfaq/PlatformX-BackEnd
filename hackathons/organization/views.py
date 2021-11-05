from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from user.models import User, Organization
from hackathons.models import Hackathon
from hackathons.serializer import GetUserHackathonsSerializer, CreateHackathonSerializer
from rest_framework.exceptions import ValidationError


# create hackathon
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_hackathon(request):
    response = {}

    try:

        # get organiztion model object
        organization = Organization.objects.get(uuid=request.user)

        serializer = CreateHackathonSerializer(data=request.data, context={"user": organization})

        if serializer.is_valid():
            print("Serializer is valid", )
            hackathon = serializer.save()
            response["success"] = "Hackathon has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response["error"] = "Error while creating hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except():
        response["error"] = "Error while creating hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get hackathons of a single organization
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_hackathons(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        hackathon_query = Hackathon.objects.filter(user=user.id).order_by('-created_at')
        hackathon_serializer = GetUserHackathonsSerializer(hackathon_query, many=True)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:

        response["error"] = "Error occurred while getting hackathon."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
