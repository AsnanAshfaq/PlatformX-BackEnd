from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    response = {}
    # creating stripe payment
    response = stripe.Charge.create(
        amount=2000,
        currency="usd",
        source="tok_amex",
        description="My First Test Charge (created for API docs)",
    )
    # store the response id in db
    # capturing stripe payment
    # capture = stripe.Charge.capture(
    #     response.id
    # )
    # print("Captured stripe id is", capture)
    return Response(data=response, status=status.HTTP_200_OK)
