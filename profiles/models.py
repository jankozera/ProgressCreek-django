from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from subscriptions.models import Subscription


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class LowercaseEmailField(models.EmailField):
    def to_python(self, value):
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    username = None
    email = LowercaseEmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["birth_date", "phone"]
    objects = CustomUserManager()
    birth_date = models.DateField()
    phone = models.CharField(max_length=20)

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    nip = models.CharField(max_length=15)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=10)
    street = models.CharField(max_length=64)
    street_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Company: {self.name}"


class CompanySubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField


class Employee(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=64)
    points = models.IntegerField()

    def __str__(self):
        return f"Employee: {self.name}"
