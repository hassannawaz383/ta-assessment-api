from django.db import models
import uuid

from apps.submissions.models import Submission


class AuditLog(models.Model):

    class ActionChoices(models.TextChoices):
        SUBMISSION_CREATED = "SUBMISSION_CREATED"
        SUBMISSION_UPDATED = "SUBMISSION_UPDATED"
        REVIEW_ADDED = "REVIEW_ADDED"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )

    actor_type = models.CharField(
        max_length=20
    )

    actor_id = models.CharField(
        max_length=255
    )

    action = models.CharField(
        max_length=50,
        choices=ActionChoices.choices
    )

    old_data = models.JSONField(
        null=True,
        blank=True
    )

    new_data = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.action