import datetime
from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from app.utils import random_string_generator
from courses.models import Course, Lesson, Question, ReadingLesson, VideoLesson
from profiles.email_service import UserMailService
from subscriptions.models import Subscription

CHOICES = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
]


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
    register_date = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    @classmethod
    @transaction.atomic
    def register(cls, user_data, company_data=None, employee_data=None):
        user = cls.objects.create_user(**user_data)
        company = None
        if company_data is not None:
            company = Company.objects.create(user=user, **company_data)

        if employee_data is not None:
            Employee.objects.create(user=user, company=company, **employee_data)

        return user

    @classmethod
    def login(cls, email, password):
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        return None

    def edit_user(self, **kwargs):
        for attr, value in kwargs.items():
            if attr == "password":
                self.set_password(value)
            else:
                setattr(self, attr, value)
        self.save()

    def add_review(self, course, rate, review):
        return Review.objects.create(
            rate=rate,
            review=review,
            user=self,
            course=course,
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

    def subscribe(self, subscription):
        CompanySubscription.objects.create(
            subscription=subscription,
            company=self,
            active=True,
        )

    def edit_company(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def invite_user(self, email):
        UserMailService.register_company_user(email, random_string_generator(), self)

    def show_employees(self):
        return self.employee_set.all()

    def __str__(self):
        return f"Company: {self.name}"


class CompanySubscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def active(self):
        return (datetime.now() - self.date).days < 365


class Employee(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=64)
    points = models.IntegerField(default=0)

    def edit_employee(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def show_course_progression(self, course):
        course_progression = CourseProgression.objects.filter(
            user=self, course=course
        ).first()
        return course_progression.progress if course_progression else 0

    def take_lesson(self, reading, video):
        course = None
        if reading is not None:
            course = reading.course
            CompletedLesson.objects.update_or_create(user=self, reading=reading)
        if video is not None:
            course = video.course
            CompletedLesson.objects.update_or_create(user=self, video=video)

        total_reading = ReadingLesson.objects.filter(course=course).count()
        total_video = VideoLesson.objects.filter(course=course).count()
        total_lessons = total_reading + total_video

        completed_lessons = CompletedLesson.objects.filter(user=self).count()

        progress = (completed_lessons / total_lessons) * 100
        CourseProgression.objects.update_or_create(
            user=self, course=course, defaults={"progress": progress}
        )

    def solve_quiz(self, quiz, user_answers):
        for question_id, user_answer in user_answers.items():
            question = Question.objects.get(id=question_id)
            UserAnswer.objects.update_or_create(
                user=self, question=question, defaults={"answer": user_answer}
            )

    def __str__(self):
        return f"Employee: {self.user.first_name}"


class CourseProgression(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField()

    def __str__(self):
        return f"Course Progression: {self.user}, {self.course}, {self.progress}"


class CompletedLesson(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reading = models.ForeignKey(
        ReadingLesson, blank=True, null=True, on_delete=models.CASCADE
    )
    video = models.ForeignKey(
        VideoLesson, blank=True, null=True, on_delete=models.CASCADE
    )


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answer = models.BooleanField()

    def __str__(self):
        return f"User answer: {self.user}, {self.question}, {self.answer}"


class Review(models.Model):
    rate = models.IntegerField(choices=CHOICES)
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review: {self.user}, {self.course}, {self.rate}"
