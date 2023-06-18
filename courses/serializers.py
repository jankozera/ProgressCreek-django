from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, Question, Quiz, ReadingLesson, VideoLesson
from profiles.models import CompletedLesson, Employee, Review
from profiles.serializers import ReviewListSerializer

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


class ReadingLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingLesson
        fields = ["id", "name", "description", "content", "created_at"]


class VideoLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLesson
        fields = ["id", "name", "description", "youtube_link", "created_at"]


class CourseRetrieveSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = 0
        reviews = Review.objects.filter(course=obj)
        count = reviews.count()
        for r in reviews:
            rating += r.rate
        if rating == 0 or count == 0:
            return rating
        return rating / count

    def get_lessons(self, obj):
        reading_lessons = ReadingLesson.objects.filter(course=obj)
        video_lessons = VideoLesson.objects.filter(course=obj)

        lessons = sorted(
            list(reading_lessons) + list(video_lessons),
            key=lambda lesson: lesson.created_at,
        )

        serialized_lessons = []
        for lesson in lessons:
            if isinstance(lesson, ReadingLesson):
                serializer = ReadingLessonSerializer
            elif isinstance(lesson, VideoLesson):
                serializer = VideoLessonSerializer

            lesson_data = serializer(lesson).data

            if self.context["request"].user.is_authenticated:
                employee = Employee.objects.filter(
                    user=self.context["request"].user
                ).first()
                completed_lesson = CompletedLesson.objects.filter(
                    user=employee,
                    reading=lesson if isinstance(lesson, ReadingLesson) else None,
                    video=lesson if isinstance(lesson, VideoLesson) else None,
                ).exists()
                lesson_data["completed"] = completed_lesson

            serialized_lessons.append(lesson_data)

        return serialized_lessons

    def get_reviews(self, obj):
        reviews = Review.objects.filter(course=obj)
        serializer = ReviewListSerializer(reviews, many=True)
        return serializer.data

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "avatar",
            "description",
            "rating",
            "lessons",
            "reviews",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "content"]


class QuizRetrieveSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz=obj)
        serializer = QuestionSerializer(questions, many=True)
        return serializer.data

    class Meta:
        model = Quiz
        fields = [
            "id",
            "course",
            "title",
            "description",
            "min_correct_answers",
            "questions",
        ]
