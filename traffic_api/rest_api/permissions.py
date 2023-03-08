from rest_framework import permissions
from django.db.models import Q

class CanCRUD(permissions.BasePermission):
    """
    Permission class for users that can perform the CRUD operations.
    """
    def has_permission(self, request, view):
        """
        Check if the user belongs to the Admin group.
        """
        if request.user and request.user.groups.filter(name='Admin'):
            return True
        return False


class CanRead(permissions.BasePermission):
    """
    Permission class for users that can perform the Read operations.
    """
    def has_permission(self, request, view):
        """
        Check if the user belongs to either Admin or Guest group.
        """
        if request.user and request.user.groups.filter(Q(name='Guest')| Q(name='Admin')):
            return True
        return False