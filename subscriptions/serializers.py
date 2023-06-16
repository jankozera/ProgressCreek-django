from django.contrib.auth import get_user_model
from rest_framework import serializers

from subscriptions.models import Subscription

User = get_user_model()


class SubscribeSerializer(serializers.Serializer):
    subscription = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all()
    )
