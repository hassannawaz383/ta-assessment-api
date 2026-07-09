from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/",
        include("apps.candidates.urls"),
        ),

    path(
        "api/v1/submissions/",
        include("apps.submissions.urls"),
        ),

    path(
        "api/v1/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
        ),
    
    path(
        "api/v1/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
        ),

    path(
        "api/v1/reviewer/",
        include("apps.reviews.urls"),
        ),
]