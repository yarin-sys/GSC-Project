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
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or obj.id == request.user.id
        )