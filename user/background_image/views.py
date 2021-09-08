from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from .serializer import BackgroundImageSerializer
from user.models import User, BackgroundImage


# creating profile image
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def create_background_image(request):
    response = {}
    # get the user
    try:
        user = User.objects.get(email=request.user)
        request.data['user'] = user.id
        serializer = BackgroundImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Background Image has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response['error'] = "Error occurred while creating Background Image"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response['error'] = "Error occurred while creating Background Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# editing post image
@api_view(['POST'])
@parser_classes([FormParser, MultiPartParser])
@permission_classes([IsAuthenticated])
def edit_background_image(request):
    response = {}
    # get the user
    try:
        user = User.objects.get(email=request.user)
        background_image_query = BackgroundImage.objects.get(user=user.id)
        request.data['user'] = user.id
        request.data['id'] = background_image_query
        serializer = BackgroundImageSerializer(background_image_query, data=request.data)
        if serializer.is_valid():
            serializer = serializer.save()
            # print("Serializer is valid", serializer.data)
            response['success'] = "Background Image has been edited"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            print(serializer)
            response['error'] = "Error occurred while editing Background Image"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        print(serializer)
        response['error'] = "Error occurred while editing Background Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# deleting post image
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_background_image(request):
    response = {}
    id = request.data['id']
    try:
        # get the id of profile image
        query = BackgroundImage.objects.get(id=id)
        query.delete()
        response['success'] = "Profile Image has been deleted successfully"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while deleting Profile Image"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
