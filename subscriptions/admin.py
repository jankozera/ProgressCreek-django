from django.contrib import admin

from subscriptions.models import Subscription, SubscriptionType

admin.site.register(SubscriptionType)
admin.site.register(Subscription)
