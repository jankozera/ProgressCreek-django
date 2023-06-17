from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course
from profiles.models import Review

User = get_user_model()


class CourseListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = 0
        reviews = Review.objects.filter(course=obj)
        count = reviews.count()
        for r in reviews:
            rating += r.rate
        if rating == 0 or count == 0:
            return rating
        return rating / count

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "avatar",
            "rating",
        ]
