from django.contrib import admin

from profiles.models import (
    Company,
    CompanySubscription,
    CourseProgression,
    Employee,
    Review,
    User,
    UserAnswer,
)

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanySubscription)
admin.site.register(Employee)
admin.site.register(CourseProgression)
admin.site.register(Review)
admin.site.register(UserAnswer)
