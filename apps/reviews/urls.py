from django.urls import path

from .views import (
    ReviewerSubmissionListView,
    ReviewSubmissionView,
)

urlpatterns = [
    path(
        "submissions/",
        ReviewerSubmissionListView.as_view(),
        name="reviewer-submissions",
    ),

    path(
        "submissions/<uuid:submission_id>/review/",
        ReviewSubmissionView.as_view(),
        name="review-submission",
    ),
]