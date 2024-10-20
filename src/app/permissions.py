from rest_framework import permissions

class IsCourseInstructor(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser: # type: ignore
            return True
        return obj.has_edit_permission(request.user)
