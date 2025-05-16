from rest_framework.permissions import BasePermission

class IsOwnerPermissionRequired(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner