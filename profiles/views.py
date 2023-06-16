from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from profiles.models import Company
from profiles.serializers import (
    AddReviewSerializer,
    InviteUserSerializer,
    LoginSerializer,
    RegisterUserSerializer,
    UpdateCompanySerializer,
    UpdateUserSerializer,
)
from subscriptions.serializers import SubscribeSerializer

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            company_data = serializer.validated_data.pop("company", None)
            employee_data = serializer.validated_data.pop("employee", None)
            user = User.register(serializer.validated_data, company_data, employee_data)
            return Response(
                {
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = User.login(
                serializer.validated_data["email"],
                serializer.validated_data["password"],
            )
            if tokens is not None:
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Invalid login credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditUserView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            user.edit_user(**serializer.validated_data)
            update_session_auth_hash(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddReviewView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        serializer = AddReviewSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data["course"]
            if course is None:
                return Response(
                    {"error": "Course does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.add_review(
                course,
                serializer.validated_data["rate"],
                serializer.validated_data["review"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeCompanyView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        company = Company.objects.filter(user=user).first()
        if company is None:
            return Response(
                {"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SubscribeSerializer(data=request.data)
        if serializer.is_valid():
            company.subscribe_company(serializer.validated_data["subscription"])
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditCompanyView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        company = Company.objects.filter(user=user).first()
        if company is None:
            return Response(
                {"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UpdateCompanySerializer(data=request.data)
        if serializer.is_valid():
            company.edit_company(**serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InviteUserView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request):
        user = request.user
        company = Company.objects.filter(user=user).first()
        if company is None:
            return Response(
                {"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = InviteUserSerializer(data=request.data)
        if serializer.is_valid():
            company.invite_user(**serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
