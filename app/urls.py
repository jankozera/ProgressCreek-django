from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/login/", TokenObtainPairView.as_view(), name="login"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
