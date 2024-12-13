from rest_framework.permissions import BasePermission
from .models import AccountType

class IsAccountType(BasePermission):
    def __init__(self, account_type):
        self.account_type = account_type

    def has_permission(self, request, view):
        # Check if the user's account type matches the required one
        return request.user.account_type == self.account_type

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

class IsMaintenance_Company(BasePermission):
    """
    Custom permission to allow access to maintenance companies only.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.account_type == AccountType.MAINTENANCE_COMPANY

