from .models import User, Student, Follower
from .serializer import UserSerializer, StudentSerializer, Users, FollowerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


# Create your views here

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        user_serializer = UserSerializer(user)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    except:
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


@api_view(['POST'])
def create_user(request):
    response = {}
    try:
        # check if username already exist
        username = User.objects.filter(username=request.data['username'])
        if username:
            response['error'] = "User name already exists"
            return Response(data=response, status=status.HTTP_200_OK)

        # check if email already exist
        email = User.objects.filter(email=request.data['email'])
        if email:
            response['error'] = "Email already exists"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # create user with given credentials
        user = User.objects.create_user(username=request.data['username'], email=request.data['email'],
                                        password=request.data['password'], first_name=request.data['first_name'],
                                        last_name=request.data['last_name'])
        if user:
            response['success'] = "Your account has been created successfully"
            return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "An error has occurred while creating your account"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    except:
        response['error'] = "An error has occurred while creating your account"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def signin(request):
    response = {}
    email = request.data['email']
    password = request.data['password']
    try:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response['email_error'] = "No Account exist with this email"
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)
        if user:
            # check for password
            if check_password(password, user.password):
                # get token
                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                response = token
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                response['password_error'] = "Password is incorrect"

                return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except:
        response['error'] = "An error occurred while signing in."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
