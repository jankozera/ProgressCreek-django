from django.contrib import admin

from profiles.models import Company, CompanySubscription, Employee, User

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanySubscription)
admin.site.register(Employee)
