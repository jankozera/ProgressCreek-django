from django.contrib.auth import get_user_model
from django.db import models

from profiles.models import Employee

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to="uploads")
    description = models.TextField()

    def __str__(self):
        return self.name


class CourseProgression(models.Model):
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField()


class Lesson(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReadingLesson(Lesson):
    content = models.TextField()


class VideoLesson(Lesson):
    youtube_link = models.CharField(max_length=256)


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    min_correct_answers = 0.8


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField()


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    answer = models.BooleanField()
