from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from user.models import User, Follower
from .serializer import FollowerSerializer, FollowedSerializer


# get follower
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request):
    response = {}
    follower_serializer = ''
    try:
        user = User.objects.get(email=request.user)  # get authenticated user
        follower_query = Follower.objects.filter(followed_id=user.id)
        follower_serializer = FollowerSerializer(follower_query, many=True)
        # if follower_serializer.is_valid():
        return Response(data=follower_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get following
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request):
    response = {}
    followed_serializer = ''
    try:
        user = User.objects.get(email=request.user)  # get authenticated user
        followed_query = Follower.objects.filter(follower_id=user.id)
        followed_serializer = FollowedSerializer(followed_query, many=True)
        return Response(data=followed_serializer.data, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# create follower
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
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# delete follower
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_follower(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)  # get authenticated user
        followed_query = Follower.objects.get(follower_id=user.id, followed_id=request.data['id'])
        if followed_query:
            followed_query.delete()
            response["success"] = "Following Removed"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Invalid Request"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occured"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
