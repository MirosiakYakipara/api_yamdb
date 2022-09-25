from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin' or request.user.is_superuser
                )))


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser))


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_authenticated
        elif view.action in ['retrieve',
                             'update',
                             'partial_update',
                             'destroy']:
            return request.user.is_authenticated
        elif view.action == 'retrive':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        request_user_is_admin: bool = False
        try:
            request_user_is_admin = request.user.role == 'admin'
        except Exception:
            pass

        request_user_is_moderator: bool = False
        try:
            request_user_is_moderator = request.user.role == 'moderator'
        except Exception:
            pass

        if view.action == 'retrieve':
            return (obj.author == request.user
                    or request_user_is_admin
                    or request_user_is_moderator)
        elif view.action == 'create':
            return True
        elif view.action in ['update', 'partial_update']:
            return (obj.author == request.user
                    or request_user_is_admin
                    or request_user_is_moderator)
        elif view.action == 'destroy':
            return (obj.author == request.user
                    or request_user_is_admin
                    or request_user_is_moderator)
        else:
            return False
