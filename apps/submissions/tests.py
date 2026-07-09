from django.test import TestCase
from rest_framework.test import APIClient

from apps.candidates.models import Candidate
from apps.assessments.models import AssessmentBrief
from apps.submissions.models import Submission


class SubmissionTests(TestCase):

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

        self.client.credentials(
            HTTP_X_CANDIDATE_TOKEN=str(
                self.candidate.private_token
            )
        )

        self.payload = {
            "assessment": str(
                self.assessment.id
            ),
            "work_link": "https://github.com/test/repo",
            "file_reference": "submission.zip",
            "time_taken_minutes": 120,
            "notes": "done",
            "challenges": "none",
        }

    def test_duplicate_submission_is_blocked(self):

        first = self.client.post(
            "/api/v1/submissions/",
            self.payload,
            format="json",
        )

        self.assertEqual(
            first.status_code,
            201
        )

        second = self.client.post(
            "/api/v1/submissions/",
            self.payload,
            format="json",
        )

        self.assertEqual(
            second.status_code,
            409
        )