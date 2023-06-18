from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Quiz
from courses.serializers import (
    CourseListSerializer,
    CourseRetrieveSerializer,
    QuizRetrieveSerializer,
)


class CourseListView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, *args, **kwargs):
        courses = Course.get_all_courses()
        serializer = CourseListSerializer(courses, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class CourseRetrieveView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, request, course_id, format=None):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseRetrieveSerializer(course, context={"request": self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizRetrieveView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, course_id, format=None):
        try:
            quiz = Quiz.objects.get(course__id=course_id)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuizRetrieveSerializer(quiz, context={"request": self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
