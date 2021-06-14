from .models import User, Student
from .serializer import UserSerializer, StudentSerializer, Users
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status


# Create your views here

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        response["error"] = "No such user exist"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    response = {}
    try:
        user = User.objects.all()
        user_serializer = Users(user, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
