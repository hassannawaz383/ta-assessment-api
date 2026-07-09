from django.urls import path

from .views import AssessmentBriefView

urlpatterns = [
    path(
        "assessment-brief/",
        AssessmentBriefView.as_view(),
        name="assessment-brief",
    ),
]