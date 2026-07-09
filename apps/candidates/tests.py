from django.test import TestCase
from rest_framework.test import APIClient

from apps.candidates.models import Candidate
from apps.assessments.models import AssessmentBrief


class AssessmentBriefTests(TestCase):

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
            is_active=True,
        )

    def test_candidate_can_fetch_assessment_with_valid_token(self):

        self.client.credentials(
            HTTP_X_CANDIDATE_TOKEN=str(
                self.candidate.private_token
            )
        )

        response = self.client.get(
            "/api/v1/assessment-brief/"
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_invalid_candidate_token_returns_401(self):

        self.client.credentials(
            HTTP_X_CANDIDATE_TOKEN="invalid-token"
        )

        response = self.client.get(
            "/api/v1/assessment-brief/"
        )

        self.assertIn(
            response.status_code,
            [401, 403]
        )
