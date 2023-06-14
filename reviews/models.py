from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Course

User = get_user_model()

CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

class Review(models.Model):
    rate = models.IntegerField(choices=CHOICES)
    review = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

