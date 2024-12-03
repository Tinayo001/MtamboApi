from rest_framework.permissions import BasePermission
from .models import AccountType

class IsDeveloper(BasePermission):
    """
    Custom permission to allow access to developers only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == AccountType.DEVELOPER

class IsTechnician(BasePermission):
    """
    Custom permission to allow access to technicians only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == AccountType.TECHNICIAN

class IsMaintenance(BasePermission):
    """
    Custom permission to allow access to maintenance companies only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == AccountType.MAINTENANCE

