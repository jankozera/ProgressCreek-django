from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to="uploads")
    description = models.TextField()

    def get_all_courses(self):
        return Course.objects.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ReadingLesson(Lesson):
    content = models.TextField()

    def __str__(self):
        return f"Reading lesson: {self.name}"


class VideoLesson(Lesson):
    youtube_link = models.CharField(max_length=256)

    def __str__(self):
        return f"Video lesson: {self.name}"


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    min_correct_answers = 0.8

    def __str__(self):
        return f"Quiz: {self.title}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return f"Question for quiz: {self.quiz}"
