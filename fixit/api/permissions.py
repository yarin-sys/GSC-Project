# api/permissions.py
from rest_framework import permissions
from django.contrib.auth import get_user_model

class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsStaffOrOwner(permissions.BasePermission):
    """
    Hanya user staff ATAU user yang mengakses data dirinya sendiri yang diizinkan.
    """

    def has_permission(self, request, view):
        # Pastikan user authenticated untuk semua operations
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff:
            return True

        # Handle berbagai tipe object
        if hasattr(obj, 'user'):  # Untuk model dengan field 'user'
            return obj.user == request.user
        elif isinstance(obj, get_user_model()):  # Untuk User object
            return obj == request.user

        # Default: tidak ada permission
        return False