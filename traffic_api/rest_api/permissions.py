from rest_framework import permissions
from django.db.models import Q

class CanCRUD(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Admin'):
            return True
        return False


class CanRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(Q(name='Guest')| Q(name='Admin')):
            return True
        return False