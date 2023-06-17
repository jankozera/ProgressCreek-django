from django.contrib import admin

from courses.models import Course, Question, Quiz, ReadingLesson, VideoLesson


class SaveAsAdmin(admin.ModelAdmin):
    save_as = True


admin.site.register(Course, SaveAsAdmin)
admin.site.register(ReadingLesson, SaveAsAdmin)
admin.site.register(VideoLesson, SaveAsAdmin)
admin.site.register(Quiz, SaveAsAdmin)
admin.site.register(Question, SaveAsAdmin)
