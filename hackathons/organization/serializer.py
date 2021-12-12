from rest_framework import serializers
from hackathons.models import Subscription
from payment.models import Payment


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class GetSubscriptionsSerializer(serializers.ModelSerializer):
    # payment = PaymentSerializer()

    class Meta:
        model = Subscription
        fields = ["id", "user", "payment_id", "plan", "created_at", "updated_at"]
