from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

import profiles.views

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/login/", profiles.views.LoginView.as_view(), name="login"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        path("api/register/", profiles.views.RegisterView.as_view(), name="register"),
        path(
            "api/update-user/",
            profiles.views.EditUserView.as_view(),
            name="update_user",
        ),
        path(
            "api/add-review/", profiles.views.AddReviewView.as_view(), name="add_review"
        ),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
