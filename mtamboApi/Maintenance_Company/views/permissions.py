from rest_framework.permissions import BasePermission

class IsAccountType(BasePermission):
    def has_permission(self, request, view):
        # your permission logic here
        return request.user and request.user.is_authenticated 

class IsMaintenanceCompany(BasePermission):
    """
    Allows access only to users with the 'maintenance_company' account type or superusers.
    """
    def has_permission(self, request, view):
        # Allow superusers full access
        if request.user.is_superuser:
            return True

        # Restrict access to users with 'maintenance_company' account type
        return request.user.is_authenticated and request.user.account_type == 'maintenance_company'

