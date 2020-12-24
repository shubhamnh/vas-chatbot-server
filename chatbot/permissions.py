from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile."""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.rno == request.user.rno

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        print (request.user)
        print (request.user.is_authenticated)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.rno == request.user.rno