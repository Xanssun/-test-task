from rest_framework import permissions

class IsObjectOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.author == request.user:
            return True
        return False

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
