import datetime

from .models import User, Student, Follower, Organization
from .serializer import UserSerializer, StudentSerializer, Users, FollowerSerializer, EditStudentSerializer, \
    UserQuerySerializer, GetStudentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException
import pyotp
import requests
from posts.models import Post
from posts.serializer import PostSerializer


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
        response["error"] = "Error occurred while getting user data"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_profile(request, id):
    response = {}
    try:
        student_query = Student.objects.get(uuid=id)
        user_serializer = GetStudentSerializer(student_query)
        return Response(data=user_serializer.data, status=status.HTTP_200_OK)

    except:
        print(user_serializer)
        response["error"] = "No such user exist"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


# get student posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_posts(request, id):
    response = {}
    try:

        # find user id
        user = User.objects.get(id=id)
        post_query = Post.objects.filter(user=user).order_by('-created_at')
        serializer = PostSerializer(post_query, many=True, context={"request": request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    except:
        response["error"] = "Couldn't get user posts"
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
        response['error'] = "Error occurred"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_student(request):
    response = {}
    try:
        # check if username already exist
        username = User.objects.filter(username=request.data['username'])
        if username:
            response['user_name'] = "User name already exists"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # check if email already exist
        email = User.objects.filter(email=request.data['email'])
        if email:
            response['email_error'] = "Email already exists"
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


# editing student
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_student(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        # check for first name
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        # check for last name
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        # check if username already exist
        if 'username' in request.data:
            username = User.objects.filter(username=request.data['username'])
            if username:
                response['user_name'] = "User name already exists"
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.username = request.data['username']
        user.save()
        student_query = Student.objects.get(uuid=user.id)
        student_serializer = EditStudentSerializer(student_query, data=request.data, partial=True)
        if student_serializer.is_valid():
            student_serializer.save()
            print(student_serializer.data)
            response['success'] = "Profile has been updated"
            return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "Error occurred while updating profile"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    except:
        response['error'] = "Error occurred while updating profile"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_organization(request):
    response = {}
    try:
        # check if email already exist
        email = User.objects.filter(email=request.data['email'])
        if email:
            response['email_error'] = "Email already exists"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        print("Trying to create user")
        # create user with given credentials
        print("Data is", request.data)
        user = User.objects.create_user(email=request.data['email'],
                                        password=request.data['password'],
                                        username=request.data['name'])
        # create organization with given credentials

        org = Organization.objects.create(uuid=user, name=request.data['name'], reg_no=request.data['reg_no'],
                                          location=request.data['location'],
                                          incorporation_date=request.data['incorporation_date'])
        if user and org:
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
    print("Email and password is", email, password)
    try:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            response['email_error'] = "No Account exists with given email address"
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


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def signout(request):
    response = {}
    try:
        # get access and refresh token
        refresh_token = request.data['refresh_token']
        access_token = request.data['access_token']
        token = RefreshToken(refresh_token)
        token.blacklist()
        response['success'] = "Successfully signing out."
        return Response(data=response, status=status.HTTP_201_CREATED)
    except:
        response['error'] = "An error occurred while signing out."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# --NOT DONE YET--


# activate user account
@api_view(['POST'])
def activate_user(request):
    print("Getting the request")
    user = User.objects.get(email=request.user)
    user.is_active = not user.is_active
    user.save()
    print(user.is_active)
    response = {'success': "Getting the request"}
    return Response(data=response, status=status.HTTP_200_OK)


# reset password
@api_view(['POST'])
def password_reset(request):
    response = {}
    try:
        user = User.objects.get(email=request.data['email'])
        subject = "Password Reset"
        # OTP instance
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        message = f"Dear User,\n\nYou are receiving this e-mail because you requested a password reset for your user " \
                  f"account at PlatformX.\n\nPlease paste the following verification code in the field provided to " \
                  f"continue.\n\nYour verification code is {otp}."
        # sending mail to user
        try:
            send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                      recipient_list=[user.email],
                      fail_silently=False)
            response['success'] = "Email has been sent successfully"
            response['otp'] = otp
            return Response(data=response, status=status.HTTP_200_OK)
        except SMTPException as e:
            print(e)
            response['email_error'] = "Error occurred while sending email"
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        response['email_error'] = "Email does not exist. Please enter a registered email"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def confirm_password_reset(request):
    response = {}
    try:
        user = User.objects.get(email=request.data['email'])
        user.password = request.data['password']
        user.save()
        response['success'] = "Password has been changed successfully"
        return Response(data=response, status=status.HTTP_201_CREATED)
    except:
        response['error'] = "Error occurred while resetting password"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bot_linked_in(request):
    res = {}
    try:
        access_token = request.data['token']

        base_url = " https://api.linkedin.com/v2/ugcPosts"

        headers = {
            "Authorization": access_token,
            "X-Restli-Protocol-Version": "2.0.0"
        }

        body = {
            "author": "urn:li:person:suAoshSJqj",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "Hello World! I am Asnan's Bot to post on linkedIn and my name is Doxi."
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        response = requests.post(base_url, headers=headers, json=body)
        if response.status_code == 201:
            res['success'] = "Content has been shared on LinkedIn"
            return Response(data=response, status=status.HTTP_201_CREATED)
        res['error'] = "Error while post on LinkedIn"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    except:
        res['error'] = "Error while post on LinkedIn"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_query(request):
    response = {}
    try:
        # get query
        query = request.data['query']
        data = {
            "query": query
        }
        serializer = UserQuerySerializer(data=data)
        if serializer.is_valid():
            response['success'] = "Your Query has been sent"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while sending query"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

    except:
        response['error'] = "Error occurred while sending query"
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
