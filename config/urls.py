from django.contrib import admin
from django.urls import path, include

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
]