from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.candidates.models import Candidate
from apps.assessments.models import AssessmentBrief
from apps.submissions.models import Submission
from apps.audit_logs.models import AuditLog
from apps.reviews.models import Review


class ReviewTests(TestCase):

    def setUp(self):

        self.client = APIClient()

        self.candidate = Candidate.objects.create(
            name="Hassan",
            email="hassan@test.com",
            city="Lahore",
        )

        self.assessment = AssessmentBrief.objects.create(
            role="BACKEND",
            title="Backend Assessment",
            description="Build APIs",
        )

        self.submission = Submission.objects.create(
            candidate=self.candidate,
            assessment=self.assessment,
            work_link="https://github.com/test/repo",
            file_reference="submission.zip",
            time_taken_minutes=120,
        )

        self.reviewer = User.objects.create_user(
            username="reviewer",
            password="password123",
            is_staff=True,
        )

        token = RefreshToken.for_user(
            self.reviewer
        )

        self.access_token = str(
            token.access_token
        )

    def test_unauthenticated_user_cannot_review_submission(self):
        self.client.credentials()
        response = self.client.post(
            f"/api/v1/reviewer/submissions/{self.submission.id}/review/",
            {
                "score": 90,
                "decision": "PASS",
                "private_note": "Good work",
                },
                format="json",
                )
        self.assertIn(
            response.status_code,
            [401, 403],
            )

    def test_review_creates_audit_log(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Bearer {self.access_token}"
        )

        response = self.client.post(
            f"/api/v1/reviewer/submissions/{self.submission.id}/review/",
            {
                "score": 92,
                "decision": "PASS",
                "private_note": "excellent",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTrue(
            Review.objects.filter(
                submission=self.submission
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                submission=self.submission,
                action="REVIEW_ADDED",
            ).exists()
        )