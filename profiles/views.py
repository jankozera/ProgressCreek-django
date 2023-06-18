from django.contrib.auth import get_user_model, update_session_auth_hash
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from profiles.models import Company, Employee, UserAnswer
from profiles.serializers import (
    AddReviewSerializer,
    CheckCourseProgressionSerializer,
    CompleteLessonSerializer,
    CurrentUserSerializer,
    InviteUserSerializer,
    LoginSerializer,
    QuizSubmitSerializer,
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


class CurrentUserView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = CurrentUserSerializer(user, context={"request": self.request})

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CheckCourseProgressionView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = CheckCourseProgressionSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.validated_data["course"]
            if course is None:
                return Response(
                    {"error": "Course does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            employee = Employee.objects.filter(user=user).first()
            if employee is None:
                return Response(
                    {"error": "You don't have employee account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                status=status.HTTP_200_OK,
                data={"progression": employee.show_course_progression(course)},
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteLessonView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = CompleteLessonSerializer(data=request.data)
        if serializer.is_valid():
            reading = (
                serializer.validated_data["reading"]
                if "reading" in serializer.validated_data
                else None
            )
            video = (
                serializer.validated_data["video"]
                if "video" in serializer.validated_data
                else None
            )
            employee = Employee.objects.filter(user=user).first()
            if employee is None:
                return Response(
                    {"error": "You don't have employee account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            employee.take_lesson(reading, video)
            return Response(status=status.HTTP_200_OK, data="Lesson completed.")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteQuizView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = QuizSubmitSerializer(data=request.data, many=True)
        if serializer.is_valid():
            employee = Employee.objects.filter(user=user).first()
            if employee is None:
                return Response(
                    {"error": "You don't have employee account"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            points = employee.solve_quiz(serializer.validated_data)
            new_total_points = 0
            all_answers = UserAnswer.objects.filter(user=employee)
            for a in all_answers:
                if a.correct:
                    new_total_points += 1
            employee.points = new_total_points
            employee.save()

            return Response(
                status=status.HTTP_200_OK,
                data=f"Quiz completed, score: {points}, total points: {employee.points}",
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
