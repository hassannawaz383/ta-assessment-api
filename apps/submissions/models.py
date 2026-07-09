from django.db import models
import uuid

from apps.candidates.models import Candidate
from apps.assessments.models import AssessmentBrief


class Submission(models.Model):

    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        REVIEWED = "REVIEWED", "Reviewed"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    assessment = models.ForeignKey(
        AssessmentBrief,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    work_link = models.URLField()

    file_reference = models.CharField(
        max_length=500,
        blank=True
    )

    time_taken_minutes = models.PositiveIntegerField()

    notes = models.TextField(
        blank=True
    )

    challenges = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["candidate", "assessment"],
                name="unique_candidate_assessment_submission"
            )
        ]

        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["submitted_at"]),
        ]

    def __str__(self):
        return f"{self.candidate.email} - {self.assessment.title}"