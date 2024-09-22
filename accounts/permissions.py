# permissions.py
from rest_framework import permissions

# is_email_exists = User.objects.filter(email=request.data.get('email')).exists()

#         if serializer.is_valid() and not is_email_exists:

class IsIncidentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access only to the owner of the incident
        return obj.reporter == request.user


class IsIncidentOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow access to the owner of the incident or admin user
        return obj.reporter == request.user or request.user.is_staff