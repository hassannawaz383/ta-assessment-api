from rest_framework import serializers

from .models import Review


class ReviewCreateSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Review

        fields = [
            "score",
            "decision",
            "private_note",
        ]

    def validate_score(
        self,
        value
    ):

        if value < 0 or value > 100:

            raise serializers.ValidationError(
                "Score must be between 0 and 100."
            )

        return value