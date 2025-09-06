from rest_framework.permissions import BasePermission

class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        # elif request.user.is_
