from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return not request.user and not request.user.is_authenticated

    message = "You must be the owner of this object dude !"
