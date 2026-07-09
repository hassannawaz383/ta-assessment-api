from rest_framework import serializers

from .models import Submission


class SubmissionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission

        fields = [
            "assessment",
            "work_link",
            "file_reference",
            "time_taken_minutes",
            "notes",
            "challenges",
        ]

    def validate_time_taken_minutes(self, value):

        if value < 1:
            raise serializers.ValidationError(
                "Time taken must be greater than zero."
            )

        if value > 10080:
            raise serializers.ValidationError(
                "Time taken exceeds maximum allowed value."
            )

        return value

    def validate_work_link(self, value):

        allowed_domains = [
            "github.com",
            "gitlab.com",
            "bitbucket.org",
            "drive.google.com",
        ]

        if not any(domain in value for domain in allowed_domains):
            raise serializers.ValidationError(
                "Unsupported work link domain."
            )

        return value