
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class HasViewPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('Store.view_history')