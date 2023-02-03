from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение для авторов, модераторов и администраторов
    на редактирование и удаление объектов.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST' and request.user.is_user:
            return True
        return request.method in ['PATCH',
                                  'DELETE'] and (request.user.is_admin
                                                 or request.user.is_moderator
                                                 or request.user == obj.author)
