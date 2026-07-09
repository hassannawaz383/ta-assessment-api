from django.db import models
import uuid


class AssessmentBrief(models.Model):

    class RoleChoices(models.TextChoices):
        BACKEND = "BACKEND", "Backend Developer"
        FRONTEND = "FRONTEND", "Frontend Developer"
        FULLSTACK = "FULLSTACK", "Full Stack Developer"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        db_index=True
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.title