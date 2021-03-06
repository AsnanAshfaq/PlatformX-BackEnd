from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from workshop.models import Workshop
from .serializer import ShareSerializer
from user.models import User


# creating share
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_share(request, ):
    response = {}
    try:
        # get the queries
        user_id = User.objects.get(email=request.user)
        workshop_query = Workshop.objects.get(id=request.data['workshop'])

        data = {
            "user": user_id.id,
            "workshop": workshop_query.id
        }
        serializer = ShareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Workshop has been shared"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while sharing workshop"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except:
        response['error'] = "Error occurred while sharing workshop"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
