from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка: является ли пользователь администратором."""
    message = 'Данное действие доступно только администратору.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.method in permissions.SAFE_METHODS
                    or request.user.is_admin)
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверяем является ли пользователь автором."""

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class OnlyAuthUserPost(permissions.BasePermission):
    """Проверка: при посте авторизован ли пользователь."""
    message = 'Только авторизованный пользователь может создать рецепт.'

    def has_object_permission(self, request, view, obj):
        return (request.method == 'POST'
                and self.context.get('request').user.is_authenticated)
