from rest_framework import serializers

from apps.assessments.models import AssessmentBrief


class AssessmentBriefSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentBrief
        fields = [
            "id",
            "role",
            "title",
            "description",
            "is_active",
        ]