from django.db import models

BASIC = "basic"
PRO = "pro"
EXPERT = "expert"

SUBSCRIPTION_TYPES = (
    (BASIC, "Basic"),
    (PRO, "Pro"),
    (EXPERT, "Expert"),
)


class SubscriptionType(models.Model):
    type = models.CharField(max_length=150, choices=SUBSCRIPTION_TYPES)
    employees_limit = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.type}, limit: {self.employees_limit}, price: {self.price}"


class Subscription(models.Model):
    type = models.OneToOneField(SubscriptionType, on_delete=models.CASCADE)
    duration = 365

    def __str__(self):
        return f"{self.type}"
