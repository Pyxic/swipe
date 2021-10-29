from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated

from account.models import User


class IsDeveloper(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role.name == 'застройщик')


class IsClient(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.role.name == 'клиент')


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        # obj here is a UserProfile instance
        return obj.id == request.user


class IsAdminOrOwner(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser
                                      or User.objects.get(id=view.kwargs['pk']) == request.user))
