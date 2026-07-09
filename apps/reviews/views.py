from django.db.models import Q

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response

from apps.reviews.models import Review

from apps.reviews.serializers import (

    ReviewCreateSerializer,

)

from apps.audit_logs.models import AuditLog

from apps.common.permissions import (

    IsReviewer,

)

from apps.submissions.models import (

    Submission,

)

from apps.submissions.serializers import (

    SubmissionListSerializer,

)


class ReviewerSubmissionListView(
    APIView
):

    permission_classes = [
        IsReviewer
    ]

    def get(
        self,
        request
    ):

        queryset = (
            Submission.objects
            .select_related(
                "candidate",
                "assessment"
            )
            .prefetch_related(
                "review"
            )
        )

        role = request.GET.get(
            "role"
        )

        status_param = request.GET.get(
            "status"
        )

        city = request.GET.get(
            "city"
        )

        submitted_after = request.GET.get(
            "submitted_after"
        )

        score_min = request.GET.get(
            "score_min"
        )

        score_max = request.GET.get(
            "score_max"
        )

        if role:
            queryset = queryset.filter(
                assessment__role=role
            )

        if status_param:
            queryset = queryset.filter(
                status=status_param
            )

        if city:
            queryset = queryset.filter(
                candidate__city=city
            )

        if submitted_after:
            queryset = queryset.filter(
                submitted_at__date__gte=submitted_after
            )

        if score_min:
            queryset = queryset.filter(
                review__score__gte=score_min
            )

        if score_max:
            queryset = queryset.filter(
                review__score__lte=score_max
            )

        serializer = (
            SubmissionListSerializer(
                queryset,
                many=True
            )
        )

        return Response(
            serializer.data
        )


class ReviewSubmissionView(APIView):

    permission_classes = [
        IsReviewer
    ]

    def post(
        self,
        request,
        submission_id
    ):

        submission = get_object_or_404(
            Submission,
            id=submission_id
        )

        serializer = ReviewCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        review = Review.objects.create(
            submission=submission,
            reviewer=request.user,
            **serializer.validated_data
        )

        submission.status = (
            Submission.StatusChoices.REVIEWED
        )

        submission.save()

        AuditLog.objects.create(
            submission=submission,
            actor_type="reviewer",
            actor_id=str(request.user.id),
            action=AuditLog.ActionChoices.REVIEW_ADDED,
            new_data={
                "score": review.score,
                "decision": review.decision,
            },
        )

        return Response(
            {
                "review_id": str(review.id),
                "score": review.score,
                "decision": review.decision,
            }
        )