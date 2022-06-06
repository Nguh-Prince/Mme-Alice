from rest_framework import permissions
import copy

class ModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map["GET"] = ["%(app_label)s.view_%(model_name)s"]

class HasPermissionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)

class IsReadingOrPostingOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or request.method == 'GET':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' or request.method == 'GET':
            return True
        return False