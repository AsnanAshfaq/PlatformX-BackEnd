from django.shortcuts import render
from django.http import HttpResponse
from .serializer import (CommentSerializer, PostSerializer, ImageSerializer)
from .models import Comment, Post, Image
from rest_framework import (viewsets, permissions, generics, status)
from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

class PostViewSet(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated]


class CommentViewSet(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ImagesViewSet(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
