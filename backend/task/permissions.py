from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Permite lectura (GET, HEAD, OPTIONS) para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite escritura solo si es el dueño de la task
        return obj == request.user
