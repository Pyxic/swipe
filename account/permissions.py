from django.db.models import Q
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from account.models import User


class IsDeveloper(IsAuthenticated):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        try:
            return bool(request.user and request.user.role.name == 'застройщик')
        except AttributeError:
            return False


class IsClient(IsAuthenticated):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return bool(request.user.role.name == 'клиент' and not request.user.banned)


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        # obj here is a UserProfile instance
        return bool(request.user.banned is False and (obj.id == request.user or obj.user == request.user))


class IsAdminOrOwner(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        # obj here is a UserProfile instance
        if request.user.is_superuser:
            return True
        return bool(request.user and not request.user.banned and (obj.id == request.user or obj.user == request.user))


class IsOwnerOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
