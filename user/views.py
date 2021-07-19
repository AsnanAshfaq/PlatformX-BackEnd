from .models import User, Student, Follower
from .serializer import UserSerializer, StudentSerializer, Users, FollowerSerializer
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
# @permission_classes([IsAuthenticated])
def get_all_users(request):
    response = {}
    try:
        user = User.objects.all()
        user_serializer = Users(user, many=True)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_follower(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)  # get authenticated user
        data = {
            "follower_id": user.id,
            "followed_id": request.data['id']
        }
        follower_serializer = FollowerSerializer(data=data)
        if follower_serializer.is_valid():
            follower_serializer.save()
            response["success"] = "Follower Added"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_follower(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)  # get authenticated user
        followed_query = Follower.objects.get(follower_id=user.id, followed_id=request.data['id'])
        if followed_query:

            data = {
                "follower_id": user.id,
                "followed_id": request.data['id']
            }
            follower_serializer = FollowerSerializer(data=data)
            if follower_serializer.is_valid():
                followed_query.delete()
                response["success"] = "Follower Removed"
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                response['error'] = "Error occured"
            return Response(data=response, status=status.HTTP_200_OK)
        response['error'] = "Invalid Request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
