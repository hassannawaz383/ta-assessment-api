from rest_framework.permissions import BasePermission


class IsCandidate(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user
            and getattr(request.user, "is_authenticated", False)
        )