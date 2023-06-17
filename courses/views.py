from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from courses.serializers import CourseListSerializer


class CourseListView(APIView):
    permission_classes = [
        permissions.AllowAny,
    ]

    def get(self, *args, **kwargs):
        courses = Course.get_all_courses()
        serializer = CourseListSerializer(courses, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
