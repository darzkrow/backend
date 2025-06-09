from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite acceso de solo lectura a usuarios no autenticados,
    y acceso completo a usuarios administradores (is_staff=True).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff

class IsEditor(permissions.BasePermission):
    """
    Permite acceso completo solo a usuarios que pertenecen al grupo 'Editores'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Editores').exists()

class IsViewer(permissions.BasePermission):
    """
    Permite solo acceso de lectura a usuarios que pertenecen al grupo 'Visualizadores'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return request.user.groups.filter(name='Visualizadores').exists()
        return False 