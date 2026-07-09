from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.authentication import (
    CandidateTokenAuthentication,
)
from apps.common.permissions import IsCandidate

from apps.assessments.models import AssessmentBrief
from .serializers import AssessmentBriefSerializer


class AssessmentBriefView(APIView):

    authentication_classes = [
        CandidateTokenAuthentication
    ]

    permission_classes = [
        IsCandidate
    ]

    def get(self, request):

        brief = AssessmentBrief.objects.filter(
            is_active=True
        ).first()

        serializer = AssessmentBriefSerializer(
            brief
        )

        return Response(serializer.data)
