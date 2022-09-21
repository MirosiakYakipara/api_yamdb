from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        # elif view.action == 'create':
        #     return request.user.is_authenticated()
        # elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
        #    return request.user.is_authenticated()
        elif view.action == 'create':
            return True
        elif view.action == 'retrive':
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if view.action == 'retrieve':
            return obj.author == request.user or request.user.is_admin
        elif view.action == 'create':
            return True
        elif view.action in ['update', 'partial_update']:
            return obj.author == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return obj.author == request.user or request.user.is_admin
        else:
            return False