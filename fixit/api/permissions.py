# api/permissions.py
from rest_framework import permissions


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

    def has_object_permission(self, request, view, obj):
        # Pastikan user authenticated
        if not (request.user and request.user.is_authenticated):
            return False

        # Staff bisa akses semua
        if request.user.is_staff:
            return True

        # Non-staff hanya bisa akses item miliknya sendiri
        # Perbaikan: obj.user bukan obj.id
        return obj.user == request.user