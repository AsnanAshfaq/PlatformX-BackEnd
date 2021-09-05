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
from rest_framework.parsers import FormParser, MultiPartParser

from rest_framework.pagination import PageNumberPagination
from user.models import User


# Create post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_post(request):
    try:
        response = {}
        print("Request data is")
        print(request.data)
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
        response["error"] = "Error while creating post"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# edit post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def edit_post(request):
    post_serializer = ''
    response = {}
    try:
        request_dict = dict(request.data)
        # check if the user is the author of the post
        post_query = Post.objects.get(id=request_dict['post'][0])
        if post_query.user != request.user:  # if user is not the author of the post then
            response["error"] = "You do not have the rights to edit this post."
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)  # return the response with error
        post_serializer = PostSerializer(post_query, data=request.data, context={"request": request})
        if post_serializer.is_valid():
            post = post_serializer.save()
            request_dict = dict(request.data)
            if 'path' in request_dict:  # check if request has path attribute
                # loop through all of the images
                # request.data['post'] = post.id
                # convert queryDict into PythonDict
                path = request_dict['path']
                metadata = request_dict['metadata']
                # loop through all the images from request and save them
                for index, path in enumerate(path):
                    # if image_query:  # if images already exist on this post
                    #     data = {
                    #         "post": request_dict['post'][0],
                    #         "path": path,
                    #         "metadata": metadata[index]
                    #     }
                    #     print("Data is")
                    #     print(data)
                    #     image_serializer = ImageSerializer(image_query[0], data=data)
                    #     if image_serializer.is_valid():
                    #         print('Saving image')
                    #         print(image_serializer.instance)
                    #         image_serializer = image_serializer.save()
                    #     else:
                    #         print(image_serializer.errors)
                    #         print("Error while updating images")
                    #         response["error"] = "Error while updating images"
                    #         return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
                    # else:
                    # create image instance
                    Image.objects.create(post=post, metadata=metadata[index], path=path)
            # post has been created with no images
            response["success"] = "Post has been edited"
            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            print(post_serializer.errors)
            response["error"] = "Post can not be edited"
            return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
    except (PermissionDenied, APIException, KeyError) as e:
        print(post_serializer)
        response["error"] = "Error while editing post"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# read all posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    try:
        response = {}
        paginator = PageNumberPagination()
        paginator.page_size = 2
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


# delete single post
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_post(request):
    response = {}
    try:
        # check if the user is the author of the post
        post_query = Post.objects.get(id=request.data['post'])
        if post_query.user != request.user:  # if user is not the author of the post then
            response["error"] = "You do not have the rights to delete this post."
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)  # return the response with error
        post_query.delete()  # delete the post
        response["success"] = "Post has been deleted"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error while deleting post"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# creating comment
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
        response["error"] = "Error while posting comment"
        return Response(data=response, status=status.HTTP_201_CREATED)


# getting comments
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
