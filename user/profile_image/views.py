from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .serializer import ProfileImageSerializer
from user.models import User, ProfileImage


# creating profile image
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def create_profile_image(request):
    response = {}
    # get the user
    try:
        user = User.objects.get(email=request.user)
        request.data['user'] = user.id
        serializer = ProfileImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Profile Image has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            response['error'] = "Error occurred while creating Profile Image"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occurred while creating Profile Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# editing post image
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def edit_profile_image(request):
    response = {}
    # get the user
    try:
        user = User.objects.get(email=request.user)
        profile_image_query = ProfileImage.objects.get(user=user.id)
        request.data['user'] = user.id
        request.data['id'] = profile_image_query
        serializer = ProfileImageSerializer(profile_image_query, data=request.data, many=True)
        if serializer.is_valid():
            response['success'] = "Profile Image has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error occurred while creating Profile Image"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occurred while creating Profile Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# deleting post image
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):
    response = {}
    id = request.data['id']
    try:
        # get the id of profile image
        query = ProfileImage.objects.get(id=id)
        query.delete()
        response['success'] = "Profile Image has been deleted successfully"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while deleting Profile Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
