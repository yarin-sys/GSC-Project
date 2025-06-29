from rest_framework import permissions
from .permissions import IsStaffEditorPermission

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAuthenticated, IsStaffEditorPermission]

class UserQuerySetMixin():
    user_field = 'user'
    allow_staff_view = True
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        
        # Handle anonymous user
        if not user.is_authenticated:
            return qs.none()
        
        # Staff dapat melihat semua data
        if self.allow_staff_view and user.is_staff:
            return qs
        
        # Non-staff hanya melihat data miliknya
        lookup_data = {self.user_field: user}
        return qs.filter(**lookup_data)