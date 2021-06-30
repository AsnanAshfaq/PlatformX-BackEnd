from django.shortcuts import render
from django.http import HttpResponse
from .serializer import (PostSerializer, CommentSerializer, ImageSerializer)
from user.serializer import UserSerializer
from .models import Comment, Post, Image
from rest_framework import (viewsets, permissions, generics, status)
from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from rest_framework.pagination import PageNumberPagination
from user.models import User


# Create post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_post(request):
    try:
        response = {}
        # return Response(data="Received data", status=status.HTTP_200_OK)
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            post = serializer.save()
            dictionary = dict(request.data)
            if 'path' in dictionary:  # check if request has path attribute
                # loop through all of the images
                # request.data['post'] = post.id
                # convert queryDict into PythonDict
                path = dictionary['path']
                metadata = dictionary['metadata']
                # loop through all the images from request and save them
                for index, path in enumerate(path):
                    image = Image.objects.create(post=post, metadata=metadata[index], path=path)
            response["success"] = "Post has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            response["error"] = "Post can not be created"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except (PermissionDenied, APIException, KeyError) as e:
        response["error"] = "Post can not be created"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get all the posts from the database
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    try:
        response = {}
        # paginator = PageNumberPagination()
        # paginator.page_size = 2
        post = Post.objects.all().order_by('-created_at')
        # result_page = paginator.paginate_queryset(post, request)
        serializer = PostSerializer(post, many=True, context={"request": request})
        # print(serializer.data[0].user)
        # user_uuid = serializer.data[0]["user"]
        # user = User.objects.get(id=user_uuid)
        # user_serializer = UserSerializer(user)
        # print(user_serializer.data)
        # return paginator.get_paginated_response(serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except AttributeError:
        response["error"] = "Error occured while gettings posts"
        return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get posts of a single user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_posts(request):
    response = {}
    post_serializer = ""
    try:
        post = Post.objects.filter(user=request.user).order_by('-created_at')
        post_serializer = PostSerializer(post, many=True, context={"request": request})
        return Response(data=post_serializer.data, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error occured while gettings posts"
        print(post_serializer)
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


class ImagesViewSet(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


@api_view(['POST'])
def create_comment(request):
    response = {}
    comment_serializer = CommentSerializer(data=request.data, context={"request": request})
    if comment_serializer.is_valid():
        print("Comment Serializer is valid")
        comment_serializer.save()
        response["success"] = "Comment has been created"
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response["success"] = "Error while posting comment"
        return Response(data=response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comments(request, id):
    response = {}
    try:
        comment = Comment.objects.filter(post=id)
        comment_serializer = CommentSerializer(comment, many=True)
        response["success"] = "Comments found"
        return Response(data=comment_serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        response["error"] = "Error while fetching comments"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
