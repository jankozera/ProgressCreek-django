from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course
from profiles.models import Company, Employee, Review

User = get_user_model()


class RegisterCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
            "nip",
            "city",
            "postal_code",
            "street",
            "street_number",
        ]


class RegisterEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "company",
            "position",
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    company = RegisterCompanySerializer(write_only=True, required=False)
    employee = RegisterEmployeeSerializer(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "phone",
            "password",
            "company",
            "employee",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "birth_date",
            "phone",
            "password",
        ]


class UpdateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "name",
            "nip",
            "city",
            "postal_code",
            "street",
            "street_number",
        ]


class InviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class AddReviewSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Review
        fields = [
            "rate",
            "review",
            "course",
        ]
