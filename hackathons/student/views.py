from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user.models import User
from .serializer import RegisterParticipantSerializer
from rest_framework.response import Response
from rest_framework import status


# register hackathon
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request, id):
    response = {}
    try:
        student = User.objects.get(email=request.user)
        data = {
            "user": student.id,
            "hackathon": id
        }
        participant_serializer = RegisterParticipantSerializer(data=data)
        if participant_serializer.is_valid():
            participant_serializer.save()
            response['success'] = "Registration Successful"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error occurred while registering for the hackathon"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except:
        response['error'] = "Bad request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
