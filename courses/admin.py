from django.contrib import admin

from courses.models import Course, Question, Quiz, ReadingLesson, VideoLesson

admin.site.register(Course)
admin.site.register(ReadingLesson)
admin.site.register(VideoLesson)
admin.site.register(Quiz)
admin.site.register(Question)
