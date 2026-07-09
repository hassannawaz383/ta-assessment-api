from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsReviewer(BasePermission):

    def has_permission(
        self,
        request,
        view
    ):

        return (
            request.user
            and isinstance(
                request.user,
                User
            )
            and request.user.is_authenticated
        )

class IsCandidate(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user
            and getattr(request.user, "is_authenticated", False)
        )