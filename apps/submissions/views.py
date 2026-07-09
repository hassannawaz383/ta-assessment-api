from django.shortcuts import render

from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.authentication import (
    CandidateTokenAuthentication,
)
from apps.common.permissions import IsCandidate

from apps.audit_logs.models import AuditLog

from .models import Submission
from .serializers import SubmissionCreateSerializer


class SubmissionCreateView(APIView):

    authentication_classes = [
        CandidateTokenAuthentication
    ]

    permission_classes = [
        IsCandidate
    ]

    def post(self, request):

        serializer = SubmissionCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:

            submission = Submission.objects.create(
                candidate=request.user,
                **serializer.validated_data
            )

        except IntegrityError:

            return Response(
                {
                    "error":
                    "submission_already_exists"
                },
                status=status.HTTP_409_CONFLICT,
            )

        AuditLog.objects.create(
            submission=submission,
            actor_type="candidate",
            actor_id=str(request.user.id),
            action=AuditLog.ActionChoices.SUBMISSION_CREATED,
            new_data={
                "status": submission.status
            },
        )

        return Response(
            {
                "id": str(submission.id),
                "status": submission.status,
            },
            status=status.HTTP_201_CREATED,
        )
