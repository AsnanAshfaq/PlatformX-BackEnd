from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from user.models import User, Organization
from hackathons.models import Hackathon, Subscription
from hackathons.serializer import GetUserHackathonsSerializer, CreateEditHackathonSerializer, PrizeSerializer, \
    CriteriaSerializer
from .serializer import CreateSubscriptionSerializer, GetSubscriptionsSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from payment.serializer import CreatePayment
from rest_framework.decorators import parser_classes
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


# create hackathon
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_hackathon(request):
    response = {}

    try:
        # get organization model object
        user = User.objects.get(email=request.user)

        organization = Organization.objects.get(uuid=request.user)

        # prepare data
        data = dict(request.data)

        logo_image = ""
        background_image = ""

        for index, path in enumerate(data['logo_image']):
            logo_image = path
        #
        for index, path in enumerate(data['background_image']):
            background_image = path

        hackathon_data = {
            "user": user,
            "title": data['title'][0],
            "tag_line": data['tag_line'][0],
            "description": data['description'][0],
            "theme_tags": data['theme_tags'],
            "rules": data['rules'],
            'resource': data['resources'],
            'submission_requirement': data['submission'][0],
            "logo_image": logo_image,
            'background_image': background_image,
            "event_date": data['event_date'][0]
        }

        serializer = CreateEditHackathonSerializer(data=hackathon_data, context={"user": organization})
        if serializer.is_valid():
            hackathon = serializer.save()

            # save prizes
            first_data = {
                "hackathon": hackathon.id,
                "title": "First",
                "value": data['first'][0]
            }
            first_prize__serializer = PrizeSerializer(data=first_data)
            if first_prize__serializer.is_valid():
                first_prize__serializer.save()

            second_data = {
                "hackathon": hackathon.id,
                "title": "Second",
                "value": data['second'][0]
            }

            second_serializer = PrizeSerializer(data=second_data)
            if second_serializer.is_valid():
                second_serializer.save()

            third_data = {
                "hackathon": hackathon.id,
                "title": "Third",
                "value": data['third'][0]
            }

            third_serializer = PrizeSerializer(data=third_data)
            if third_serializer.is_valid():
                third_serializer.save()

            # save judging criteria
            for index, title in enumerate(data['criteria_title']):
                title = title
                description = data['criteria_description'][index]

                criteria_data = {
                    "hackathon": hackathon.id,
                    "title": title,
                    "description": description
                }

                criteria_serializer = CriteriaSerializer(data=criteria_data)
                if criteria_serializer.is_valid():
                    criteria_serializer.save()

            response["success"] = "Hackathon has been created"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response["error"] = "Error occurred while creating hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except:
        response["error"] = "Error occurred while creating hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# edit hackathon
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_hackathon(request):
    response = {}
    try:
        # get hackathon id
        hackathon_query = Hackathon.objects.get(id=request.data["hackathon_id"])
        # get organization model object
        organization = Organization.objects.get(uuid=request.user)
        serializer = CreateEditHackathonSerializer(hackathon_query, data=request.data, context={"user": organization})
        if serializer.is_valid():
            hackathon = serializer.save()
            response["hackathon_id"] = hackathon.id
            response["success"] = "Hackathon has been edited"
            return Response(data=response, status=status.HTTP_200_OK)
        response["error"] = "Error occurred while editing hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    except():
        response["error"] = "Error occurred while editing hackathon"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# get hackathons of an organization
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organization_hackathons(request):
    response = {}
    try:
        user = User.objects.get(email=request.user)
        hackathon_query = Hackathon.objects.filter(user=user.id).order_by('-created_at')
        hackathon_serializer = GetUserHackathonsSerializer(hackathon_query, many=True)
        return Response(data=hackathon_serializer.data, status=status.HTTP_200_OK)
    except:
        response["error"] = "Error occurred while getting hackathon."
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# subscribe to hackathon subscription service
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe(request):
    response = {}
    try:

        user = User.objects.get(email=request.user)
        org_user = Organization.objects.get(uuid=user.id)
        amount = int(request.data['charges']) * 100 * 0.43
        plan = request.data['plan']

        # make stripe payment
        description = f"Subscribed to hackathon plan {plan}."
        stripe_response = stripe.Charge.create(
            amount=int(amount),
            currency="inr",
            source="tok_visa",
            description=description,
            receipt_email=user.email
        )

        payment_data = {
            "user": user.id,
            "charge_id": stripe_response['id']
        }

        payment_serializer = CreatePayment(data=payment_data)
        if payment_serializer.is_valid():
            # add data in payment
            payment = payment_serializer.save()
            subscription_data = {
                "user": org_user,
                "plan": plan,
                "payment_id": payment.id,
            }

            # add data in subscription
            subscription_serializer = CreateSubscriptionSerializer(data=subscription_data)
            if subscription_serializer.is_valid():
                subscription_serializer.save()
                response['success'] = "Subscription successful"
                return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "Subscription error."
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)

    except:
        response['error'] = "Subscription error."
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_subscription(request):
    # getting user subscriptions
    response = {}
    try:

        user = User.objects.get(email=request.user)
        org_user = Organization.objects.get(uuid=user.id)
        subscription_query = Subscription.objects.filter(user=org_user.uuid)
        serializer = GetSubscriptionsSerializer(subscription_query, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    except:
        print(serializer)
        response['error'] = "Subscription error."
        return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
