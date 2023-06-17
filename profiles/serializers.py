from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, ReadingLesson, VideoLesson
from profiles.models import Company, CompanySubscription, Employee, Review

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


class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]


class CurrentUserCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "nip",
            "city",
            "postal_code",
            "street",
            "street_number",
        ]


class CurrentUserEmployeeSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    def get_employess(self, obj):
        employees = obj.show_employees()
        serializer = EmployeeUserSerializer(employees, many=True)
        return serializer.data

    class Meta:
        model = Employee
        fields = [
            "id",
            "position",
            "points",
            "employees",
        ]


class CurrentUserSerializer(serializers.ModelSerializer):
    company = CurrentUserCompanySerializer(read_only=True)
    employee = CurrentUserEmployeeSerializer(read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_subscription(self, obj):
        subscription = False
        company = Company.objects.filter(user=obj).first()
        if company is not None:
            company_sub = CompanySubscription.objects.filter(company=company).first()
            if company_sub is not None:
                if company_sub.active:
                    subscription = True
        employee = Employee.objects.filter(user=obj).first()
        if employee is not None:
            emp_company_sub = CompanySubscription.objects.filter(
                company=employee.company
            ).first()
            if emp_company_sub is not None:
                if emp_company_sub.active:
                    subscription = True

        return subscription

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "birth_date",
            "phone",
            "company",
            "employee",
            "subscription",
        ]


class ReviewListSerializer(serializers.ModelSerializer):
    user = EmployeeUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "user",
            "review",
            "rate",
        ]


class CheckCourseProgressionSerializer(serializers.Serializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())


class CompleteLessonSerializer(serializers.Serializer):
    reading = serializers.PrimaryKeyRelatedField(
        queryset=ReadingLesson.objects.all(), required=False
    )
    video = serializers.PrimaryKeyRelatedField(
        queryset=VideoLesson.objects.all(), required=False
    )
