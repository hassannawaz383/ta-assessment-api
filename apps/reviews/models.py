from django.db import models
from django.contrib.auth.models import User
import uuid

from apps.submissions.models import Submission


class Review(models.Model):

    class DecisionChoices(models.TextChoices):
        PASS = "PASS", "Pass"
        FAIL = "FAIL", "Fail"
        HOLD = "HOLD", "Hold"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name="review"
    )

    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="reviews"
    )

    score = models.PositiveSmallIntegerField()

    decision = models.CharField(
        max_length=10,
        choices=DecisionChoices.choices
    )

    private_note = models.TextField(
        blank=True
    )

    reviewed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["score"]),
            models.Index(fields=["decision"]),
        ]

    def __str__(self):
        return f"{self.submission_id} - {self.decision}"