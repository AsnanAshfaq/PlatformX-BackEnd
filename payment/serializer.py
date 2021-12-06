from rest_framework import serializers
from .models import Payment
from datetime import datetime


class CreatePayment(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
