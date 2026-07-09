from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.candidates.models import Candidate


class CandidateTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.headers.get("X-Candidate-Token")

        if not token:
            return None

        try:
            candidate = Candidate.objects.get(
                private_token=token
            )

        except Candidate.DoesNotExist:
            raise AuthenticationFailed(
                "Invalid candidate token."
            )

        return (candidate, None)