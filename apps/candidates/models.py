from django.db import models
import uuid


class Candidate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(
        unique=True
    )

    city = models.CharField(
        max_length=100
    )

    private_token = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["private_token"]),
            models.Index(fields=["city"]),
        ]

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email